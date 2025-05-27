# 1. 采样(Sampling)
### 1.1 采样

扫描像素中心点坐标，判断是否在三角面片内部，中心点即为采样点

<center><img alt=图 0 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748333458531.png width=400></center>

判断方法：
<center><img alt=图 1 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748333720274.png width=400></center>

$$
\begin{matrix}
    \triangle ABC:\boldsymbol{AB}\times\boldsymbol{AP},\boldsymbol{BC}\times\boldsymbol{BP},\boldsymbol{CA}\times\boldsymbol{CP}方向相同时，P在\triangle ABC内 \\
    \boldsymbol{AB},\boldsymbol{BC},\boldsymbol{CA}首尾相接
\end{matrix}
$$

>边缘上的点处理方法比较灵活，OpenGL和DirectX将左边和上边定义在三角形内

一种较为优化的扫描方法：
<center><img alt=图 2 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748341578740.png width=400></center>


### 1.2 走样（aliasing）

<center>
<img alt=图 5 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748341863576.png width=200/>
<img alt=图 3 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748341694812.png width=200/>
</center>

>光栅化后的图有明显的锯齿边缘

<center><img alt=图 7 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748343037009.png width = 500></center>

>**走样**定义为不同函数采样结果相同

### 1.3 反走样（Antialiasing）
采样频率低于变换频率会发生Artifacts
 
 <center><img alt=图 6 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748342621514.png></center>
 
 **解决方式**：对原始图像滤波（模糊）后采样

#### 1.3.1 滤波
>**滤波**定义为对函数进行傅里叶级数展开后抹除一些特定频率的级数项

对图片进行傅里叶变换得到频谱图
<center><img alt=图 8 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748343725163.png width=500></center>

**高通滤波**（High-pass filter）：
<center><img alt=图 9 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748343798509.png width=500></center>

**低通滤波**
<center><img alt=图 10 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748344253982.png width=500></center>

**卷积**（Box filter）:
<center><img alt=图 11 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748344551115.png width=500></center>

>卷积也是一种低通滤波

#### 1.3.2 MSAA (MultiSamplingAntiAliasing)
对每一个像素求平均值（卷积）
<center><img alt=图 12 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748344897846.png width=500></center>

<center><img alt=图 13 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748345039623.png width=400></center>

在一个像素内有多个采样点 

**采样后**：
<center><img alt=图 14 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748345122233.png width=400></center>

# 2. 深度测试

### 2.1 深度缓存
>用于解决不同面片遮挡关系

<center><img alt=图 15 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748346005108.png width=400></center>
对每个像素创建深度缓存

>透明物体无法使用深度缓存解决，需要特殊处理