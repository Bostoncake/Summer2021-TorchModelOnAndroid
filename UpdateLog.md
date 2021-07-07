# Update Logs

## 7-7-21

- Find a detection model checkpoint with corresponding PyTorch file.
  - I couldn't find any modern models directly inheriting nn.Module, most models consist of many objects inherited from nn.Module.
  - Maybe we could use Faster-RCNN from official PyTorch modules. But can the pruning framework support Faster-RCNN?
  - What is the **input** and **output** of TorchPruner?
- Look into PyTorch Mobile.
  - Found a link dealing with the issue: https://pytorch.org/mobile/android/

