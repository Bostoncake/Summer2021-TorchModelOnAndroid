from darknet import Darknet
import torch

model = Darknet("cfg/yolov3.cfg")
yolov3_state_dict = torch.load('yolov3.pt')
model.load_state_dict(yolov3_state_dict)