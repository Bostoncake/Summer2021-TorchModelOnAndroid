# YOLO v3 implementation

从零开始实现YOLO v3：https://blog.paperspace.com/how-to-implement-a-yolo-object-detector-in-pytorch/

## How does it work?

- 单阶段检测算法，速度非常快，在经过不断改进之后达到了相当的检测精度；
- YOLO 发展史：
  - YOLO v1：具有开创性地做出来了单阶段检测的工作，最大的特点就是“快”--从图片的输入直达7\*7\*30的输出结构，直接回归出output而不需要一个额外的阶段生成RP；
  - YOLO v2：在YOLO v1的结构基础上加了一大堆的trick（聚类提取anchor，BN等）；
  - YOLO v3：进一步的改进提升速度，和SSD相同的准确率，但速度快三倍；使用53层的残差单元叠加而成的卷积网络，比ResNet，Darknet-19表现更好；