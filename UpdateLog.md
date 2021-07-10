# Update Logs

## 7-7-21

- Find a detection model checkpoint with corresponding PyTorch file.
  - I couldn't find any modern models directly inheriting nn.Module, most models consist of many objects inherited from nn.Module.
  - Maybe we could use Faster-RCNN from official PyTorch modules. But can the pruner framework support Faster-RCNN?
  - What is the **input** and **output** of TorchPruner?
- Look into PyTorch Mobile.
  - Found a link dealing with the issue: https://pytorch.org/mobile/android/

## 7-10-21

- Investigated into YOLO v3 and YOLO v4. The models are basically one-stage detectors with fair bells-and-whistles. Maybe could attach the pruner on YOLO v3. 
- Find a guide on implementing YOLO v3 from scratch. Try to implement the model under PyTorch framework.