# YOLO v3 implementation

从零开始实现YOLO v3：https://blog.paperspace.com/how-to-implement-a-yolo-object-detector-in-pytorch/

Corresponding GitHub repo: https://github.com/ayooshkathuria/YOLO_v3_tutorial_from_scratch

## How does it work?

- 单阶段检测算法，速度非常快，在经过不断改进之后达到了相当的检测精度；
- YOLO 发展史：
  - YOLO v1：具有开创性地做出来了单阶段检测的工作，最大的特点就是“快”--从图片的输入直达7\*7\*30的输出结构，直接回归出output而不需要一个额外的阶段生成RP；
  - YOLO v2：在YOLO v1的结构基础上加了一大堆的trick（聚类提取anchor，BN等）；
  - YOLO v3：进一步的改进提升速度，和SSD相同的准确率，但速度快三倍；使用53层的残差单元叠加而成的卷积网络，比ResNet，Darknet-19表现更好；

## How to implement from scratch?

- 网络结构：使用`.cfg`文件进行定义，使用官方提供的config文件构建网络，cfg文件的读取需要写一个简单的函数；
- 使用`nn.ModuleList`（按照模块进行排列，但需要手动注册`forward`）注册网络，其与`nn.Sequential`（按照模块进行排列，默认可以自动`forward`）的区别与联系可以参考：https://zhuanlan.zhihu.com/p/75206669；
- Some layers in DarkNet:
  - Shortcut: 将不同层之间的卷积输出相连，类似于残差块，但是权重和连接方式随不同的backbone而不同；
  - Upsample: 上采样层，DarkNet采用双线性插值上采样；
  - Route: 路由层，实际上就是把几个层拼在一起（concatenate）；
  - YOLO: 检测层，网络中一共有3个，分别在不同的尺度完成检测任务；
- Tricks in implementing the layers:
  - Track filter numbers of all preceding layers: depth of kernels in upcoming layers require the information;
  - A block contains many layers;
  - As for route layer: use dummy layer to represent it in nn.Module, but define calculation in `forawrd` function;
- Tricks in implementing forward pass:
  - `contiguous()` after using `transpose()` in tensor re-shaping: make the re-shaped tensor occupying an independent memory space;
  - `view()` does not change the actual arrangement of data; note that `view()` is a torch function;
  - Usage of some numpy functions: `meshgrid()`, `reshape()`; some torch functions: `unsqueeze()` as well;
- Doing forward tests:
  - Change the img input size to the size mentioned in cfg file;
  - ALL TENSORS SHOULD BE ON GPU IF CUDA USED!!!!
- Using official weights;
- When input is 416\*416, output is 1\*10647\*85, input 608\*608 and output is 1\*22743\*85;
- 

  