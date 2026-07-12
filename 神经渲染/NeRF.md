# 1. 经典NeRF

## 1.1 基本思想

> NeRF将场景看作一个辐射场，每个点都有一个颜色和一个密度（单位长度消光系数），颜色在五维辐射场中采样，密度在三维辐射场中采样。照片像素就是对该辐射场某一射线上的区域进行积分的结果。使用MLP网络拟合辐射场分布，最终得到4个函数 $g_r/g_g/g_b(x,y,z, d_x, d_y, d_z),g_\sigma(x,y,z)$ ，其中 $d_x, d_y, d_z$ 是归一化方向，$x,y,z$ 是空间坐标, $\sigma$ 是单位长度消光系数(体密度)。

<center><img alt=图 0 src=../images/NeRF1783833631206.png width=400></center>

>NeRF假设照片是对一个辐射场进行采样的结果。图上是将一个彩色物体拆解为4个分布：红色/绿色/蓝色五维分布和密度三维分布。MLP网络可以拟合这4个分布。

<center><img alt=图 2 src=../images/NeRF1783835281904.png></center>

>g(x):MLP，f(x):真实分布，照片的像素是f(x)在某一区间上的积分，体渲染结果就是在该区间上进行采样求和。最后计算loss，训练MLP不断接近f(x)。

## 1.2 数学原理

<center><img alt=图 4 src=../images/NeRF1783843666031.png></center>

$$\hat{C(s)} = \int_{0}^{+\infty} T(s)\sigma(s)C(s) ds$$



- $T(s)$ 是在s点之前，剩余光线比例。$T(s) = e^{-\int_{0}^{s}\sigma(t)dt}$。
- $\sigma(s)$ 在s点的消光系数。
- $C(s)$ 在s处的点颜色。
- $\frac{dT}{ds} = -\sigma(s)T(s)$。

**离散化后的公式**

$$\hat{C(s)} = \sum_{i=1}^{N} T_i(1-e^{-\sigma_i\delta_i})c_i$$

- $T_i$ 是在第i个点之前，剩余光线比例。
- $\sigma_i$ 是第i个点的光线的消光系数。
- $\delta_i$ 是第i个点到s点的距离。
- $c_i$ 是第i个点的颜色。
- $N$ 是采样的点的数量。

## 1.3网络结构

<center><img alt=图 3 src=../images/NeRF1783842178168.png></center>

$\gamma(p) = (sin(2^0\pi p), cos(2^0\pi p), sin(2^1\pi p), cos(2^1\pi p), ..., sin(2^{L-1}\pi p), cos(2^{L-1}\pi p))$

>位置编码

- $\gamma(x)$ : $3\times 2 \times 10 + 3 = 63$
- $\gamma(d)$ : $3\times 2 \times 4 + 3 = 27$

## 1.4 训练与推理

<center><img alt=图 6 src=../images/NeRF1783848533453.png></center>

1. 输入n个相机拍摄的照片，得到 $n\times w \times h$ 个射线。
2. 对射线进行均匀采样，得到 $n\times w \times h \times 64$ 个采样点。
3. 分批次输入到粗模型中，得到 $(\sigma_i^c, c_i^c)$ 作为粗模型的输出。
4. 根据粗模型输出的 $(\sigma_i^c, 64)$ ，计算概率分布 $p_i = \frac{w_i^c}{\sum_j w_j^c}$ 。
5. 重新进行重要性采样，采集128个点，与64个点合并成 $(x,y,z, d_x, d_y, d_z, 192)$，作为细模型的输入。
6. 使用粗模型和细模型的输出进行体渲染，计算loss：$\mathcal{L} = \sum\limits_r \| \hat{C_c}(r) - C_{gt}(r) \|_2^2 + \sum\limits_r \| \hat{C_c}(f) - C_{gt}(r) \|_2^2$

## 1.5 基本假设

- 采样点周围1/2间隔空间内，体密度 $\sigma$ 不变，颜色和观察方向有关。所以位置信息使用8层网络进行特征提取，而方向信息只在计算颜色时使用一层网络。

# 展望

- Instant-NGP 哈希网络代替MLP
- mip-NeRF/mip-NeRF 360 抗锯齿与无界场景
- TensorRF 显式特征与低秩分解
- Neus/VolSDF 辐射场+SDF表面
- D-NeRF/Nerfies: 时间和规范空间形变
- 稀疏视图NeRF
- ...