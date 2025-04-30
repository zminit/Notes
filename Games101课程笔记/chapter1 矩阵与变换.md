# 1. 向量运算
**点乘**：$\vec{a} \cdot \vec{b}$
$$
\begin{align}
    (x_1,y_1) \cdot (x_2, y_2) = x_1* x_2+y_1*y_2 \\
    (x_1,y_1) \cdot (x_2, y_2) = ||\vec{a}|| \cdot ||\vec{b}|| \cdot \cos\theta
\end{align}
$$

**叉乘**：$\vec{a} \times \vec{b}$
$$
\begin{align}
    ||\vec{a} \times \vec{b}|| = ||\vec{a}||\cdot ||\vec{b}|| \cdot \sin\theta\\
    (x_1, y_1) \times (x_2, y_2) = 
    \begin{vmatrix}
        \vec{i} & \vec{j} & \vec{k} \\
        x_1 & y_1 & 0 \\
        x_2 & y_2 & 0
    \end{vmatrix}
\end{align}
$$


# 2. 变换矩阵
### 2.1 缩放矩阵
$$
\begin{matrix}
    x^\prime = s_x \cdot x \\
    y^\prime = s_y \cdot y \\
    \begin{bmatrix}
        x^\prime \\
        y^\prime
    \end{bmatrix}
    = 
    \begin{bmatrix}
        s_x & 0 \\
        0 & s_y
    \end{bmatrix}
    \begin{bmatrix}
        x\\
        y
    \end{bmatrix}
\end{matrix}
$$
$s_x为x坐标缩放比例，s_y为y坐标缩放比例$

### 2.2 对称矩阵
特殊的缩放矩阵
$$
\begin{matrix}
    \begin{bmatrix}
        -1 & 0\\
        0 & 1
    \end{bmatrix}
    &
    \begin{bmatrix}
        1 & 0\\
        0 & -1
    \end{bmatrix}
    &
    \begin{bmatrix}
        -1 & 0\\
        0 & -1
    \end{bmatrix} \\
    关于y轴对称 & 关于x轴对称 &中心对称\\
    x坐标反转 & y坐标反转 & x,y坐标反转
\end{matrix}
$$

### 2.3 切变矩阵
$$
\begin{bmatrix}
    1 & a \\
    b & 1
\end{bmatrix}
$$
<center><img src="./附件/image.png" width="250"></center>

### 2.4 旋转矩阵
$$
\begin{matrix}
    \begin{bmatrix}
    \cos\theta & -\sin\theta \\
    \sin\theta & \cos\theta
    \end{bmatrix} \\
    \theta 为逆时针旋转的角度
\end{matrix}
$$ 

# 3. 仿射变换
### 3.1 其次坐标
为了解决平移问题无法使用矩阵表示的问题，引入其次
$$
$$

