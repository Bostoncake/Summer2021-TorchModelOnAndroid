from __future__ import division

import torch 
import torch.nn as nn
import torch.nn.functional as F 
from torch.autograd import Variable
import numpy as np


# Dummy layer for route and shortcut layers
class EmptyLayer(nn.Module):
    def __init__(self):
        super(EmptyLayer, self).__init__()

# Final layer doing detection process
class DetectionLayer(nn.Module):
    def __init__(self, anchors):
        super(DetectionLayer, self).__init__()
        self.anchors = anchors


def parse_cfg(cfgfile):
    """
        Reads the config file and returns corresponding values.
    """

    file = open(cfgfile, 'r')
    lines = file.read().split('\n')
    lines = [x for x in lines if len(x) > 0]
    lines = [x for x in lines if x[0] != '#']
    lines = [x.rstrip().lstrip() for x in lines]

    block = {}
    blocks = []

    for line in lines:
        if line[0] == "[":                      # This marks the start of a new block
            if len(block) != 0:                 # If block is not empty, implies it is storing values of previous block.
                blocks.append(block)            # add it the blocks list
                block = {}                      # re-init the block
            block["type"] = line[1:-1].rstrip()     
        else:
            key,value = line.split("=") 
            block[key.rstrip()] = value.lstrip()
    blocks.append(block)

    return blocks

def create_modules(blocks):
    
    net_info = blocks[0]                        # Stores the net info
    module_list = nn.ModuleList()
    prev_filters = 3                            # input images have 3 channels
    output_filters = []

    for index, x in enumerate(blocks[1:]):
        module = nn.Sequential()

        # create new modules for corresponding blocks

        if (x["type"] == "convolutional"):
            activation = x["activation"]
            try:
                batch_normalize = int(x["batch_normalize"])
                bias = False
            except:
                batch_normalize = 0
                bias = True

            filters= int(x["filters"])
            padding = int(x["pad"])
            kernel_size = int(x["size"])
            stride = int(x["stride"])

            if padding:
                pad = (kernel_size - 1) // 2
            else:
                pad = 0

            #Add the convolutional layer
            conv = nn.Conv2d(prev_filters, filters, kernel_size, stride, pad, bias = bias)
            module.add_module("conv_{0}".format(index), conv)

            #Add the Batch Norm Layer
            if batch_normalize:
                bn = nn.BatchNorm2d(filters)
                module.add_module("batch_norm_{0}".format(index), bn)

            #Check the activation. 
            #It is either Linear or a Leaky ReLU for YOLO
            if activation == "leaky":
                activn = nn.LeakyReLU(0.1, inplace = True)
                module.add_module("leaky_{0}".format(index), activn)

        elif (x["type"] == "upsample"):
            # Use bilinear upsampling for upsample layers
            stride = int(x["stride"])
            upsample = nn.Upsample(scale_factor = 2, mode = "bilinear")
            module.add_module("upsample_{0}".format(index), upsample)

        elif (x["type"] == "route"):
            x["layers"] = x["layers"].split(',')
            start = int(x["layers"][0])
            try:
                end = int(x["layers"][1])
            except:
                end = 0
            #Positive anotation
            if start > 0: 
                start = start - index
            if end > 0:                 # only when presented in non-relative index
                end = end - index
            route = EmptyLayer()
            module.add_module("route_{0}".format(index), route)
            if end < 0:
                filters = output_filters[index + start] + output_filters[index + end]
            else:                       # only when no end existed
                filters= output_filters[index + start]

        #shortcut corresponds to skip connection
        elif x["type"] == "shortcut":
            shortcut = EmptyLayer()
            module.add_module("shortcut_{}".format(index), shortcut)

        elif x["type"] == "yolo":

            # get first 3 tuples
            mask = x["mask"].split(",")
            mask = [int(x) for x in mask]

            anchors = x["anchors"].split(",")
            anchors = [int(a) for a in anchors]
            anchors = [(anchors[i], anchors[i+1]) for i in range(0, len(anchors),2)]
            anchors = [anchors[i] for i in mask]

            detection = DetectionLayer(anchors)
            module.add_module("Detection_{}".format(index), detection)
        
        module_list.append(module)
        prev_filters = filters
        output_filters.append(filters)

    return (net_info, module_list)

blocks = parse_cfg("cfg/yolov3.cfg")
print(create_modules(blocks))