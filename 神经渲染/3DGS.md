# 1. 3DGS

## 1.1 前置基础

### 1.1.1 线性代数基础

$$\exist A, A^T = A 且 A可逆 \Leftrightarrow \exist V, V^T V = I, \det(V) = 1, A = V^T \Lambda V$$

$$R是旋转矩阵 \Leftrightarrow R^T R = I, \det(R) = 1$$

$$线性：f(x_1+x_2)=f(x_1)+f(x_2)$$

### 1.1.2 高斯分布

$$G(x)=\frac{1}{\sqrt{(2\pi)^k|\Sigma|}}e^{-\frac{1}{2}(x-\mu)^T\Sigma^{-1}(x-\mu)}$$

- $x=[x,y,z]^T$ 是空间中采样点。
- $\mu=[\mu_x,\mu_y,\mu_z]^T$ 是均值向量，也是高斯球中心位置。
- $\Sigma$ 是协方差矩阵, 半正定，控制高斯球大小，形状和朝向。
- $G(x)\in (0,1]$ 该高斯在x处的概率密度。
- $\frac{1}{\sqrt{(2\pi)^k|\Sigma|}}$ 是归一化因子，确保高斯分布在空间中积分为1，但3DGS一般不使用。



**协方差矩阵**
>协方差矩阵与几何变换的关系

3DGS只是用了高斯分布的几何属性，因此这里只需要将协方差矩阵当作特殊的对称矩阵就行。

$$\Sigma = \begin{bmatrix}
    \sigma_x^2 & \sigma_{xy} & \sigma_{xz} \\
    \sigma_{xy} & \sigma_y^2 & \sigma_{yz} \\
    \sigma_{xz} & \sigma_{zy} & \sigma_z^2
   \end{bmatrix}$$

- $\Sigma^T = \Sigma, v^T \Sigma v \geq 0$, 对称半正定。
- 一个三维协方差矩阵需要 $(\sigma_x,\sigma_y,\sigma_z,\sigma_{xy},\sigma_{xz},\sigma_{yz},\sigma_{zy},)$ 6个参数确定。
- 根据线代基础，$\Sigma = V^T \Lambda V$，其中$V$是正交矩阵，$\Lambda$是对角矩阵，$V^T = V^{-1}$， $V$ 是旋转矩阵， $\Lambda$ 是缩放矩阵。

已知 $(\lambda_x, \lambda_y, \lambda_z, x, y, z, w)$ ，求 $\Sigma$。

$$R(q) = \begin{bmatrix}
    1-2y^2-2z^2 & 2xy-2wz & 2xz+2wy \\
    2xy+2wz & 1-2x^2-2z^2 & 2yz-2wx \\
    2xz-2wy & 2yz+2wx & 1-2x^2-2y^2
   \end{bmatrix}$$

$$\Sigma = R \begin{bmatrix}
    \lambda_x^2 & 0 & 0 \\
    0 & \lambda_y^2 & 0 \\
    0 & 0 & \lambda_z^2
   \end{bmatrix}R^T$$

**高斯球**
>高斯球的几何属性

$$G(x) = e^{-\frac{1}{2}(x-\mu)^T\Sigma^{-1}(x-\mu)}$$

$$令y = (x-\mu)^TR,(x-\mu)^T\Sigma^{-1}(x-\mu) =  y^T V y =\frac{y_1^2}{\lambda_x^2} + \frac{y_2^2}{\lambda_y^2} + \frac{y_3^2}{\lambda_z^2} = constant$$

<center><img alt=图 2 src=../images/3DGS1783941677490.png width=400></center>

- $G(x) = C$ 就是一个椭球壳，所以 $G(x) \in (0,1]$ 代表一个椭球体,同时值从中心向外快速衰减。

<center><img alt=图 0 src=../images/3DGS1783931448956.png width=400></center>

- 从图中可以看到 $G(x)$ 是一个无限延申的函数，一般使用 $G = e^{-k^2/2}$ 作为截断处。实际应用会有所不同。

**高斯球性质**

- 仿射变换高斯核仍然闭合。
- 高斯核沿着某一个轴积分降维后，仍然是高斯。
- 高斯核是一个实心椭球，每一层代表一个概率。

### 1.1.3 雅可比矩阵

<center><img alt=图 1 src=../images/3DGS1783941599165.png width=400></center>

- 非线性变换会破坏函数的性质（如图上的正方形变换后变得扭曲），我们可以在局部微小空间中使用线性变换近似非线性变换（如图上橙色虚线），来保留一些性质。

$$F:\mathbb{R}^3 \to \mathbb{R}^3, F(x) = \begin{bmatrix}
    F_1(x) \\
    \dots \\
    F_3(x)
\end{bmatrix}$$

$$J_F(\vec{x}) = \begin{bmatrix}
    \frac{\partial F_1}{\partial x_1} & \dots & \frac{\partial F_1}{\partial x_3} \\
    \dots & & \dots  \\
    \frac{\partial F_3}{\partial x_1} & \dots & \frac{\partial F_3}{\partial x_3}
\end{bmatrix}$$
 
 $$F(x+\Delta x) \approx F(x) + J_F(x)\Delta x$$

**基函数与球谐函数**

