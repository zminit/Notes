# 1. 向量运算
**点乘**： $\vec{a} \cdot \vec{b}$

$$
\begin{align}
    (x_1,y_1) \cdot (x_2, y_2) = x_1* x_2+y_1*y_2 \\
    (x_1,y_1) \cdot (x_2, y_2) = ||\vec{a}|| \cdot ||\vec{b}|| \cdot \cos\theta
\end{align}
$$

**叉乘**： $\vec{a} \times \vec{b}$

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

<center><img src="../images/2025051400.png" width="250"></center>

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

>旋转矩阵为正交矩阵

# 3. 仿射变换
### 3.1 齐次坐标
为了解决平移问题无法使用矩阵表示的问题，引入齐次坐标，这里第三维区别在平移矩阵笔记小结讲解

$$
\begin{matrix}
    向量：\vec{a} = (x,y,0) \\
    坐标点：a = (x,y,1) 
\end{matrix}
$$
非齐次坐标平移变换：
$$
\begin{bmatrix}
    x^\prime \\ y^\prime
\end{bmatrix} =
\begin{bmatrix}
    1 & 0 \\ 
    0 & 1
\end{bmatrix}
\begin{bmatrix}
    x \\ y
\end{bmatrix}
+
\begin{bmatrix}
    t_x \\ t_y
\end{bmatrix}
$$

### 3.2 平移矩阵

$$
\begin{matrix}
    \begin{cases}
        x^\prime = x + t_x \\
        y^\prime = y + t_y
    \end{cases} \\ \\
    坐标点平移：
    \begin{bmatrix}
        x^\prime \\ y^\prime \\ 1
    \end{bmatrix} = 
    \begin{bmatrix}
        1 & 0 & t_x \\
        0 & 1 & t_y \\
        0 & 0 & 1
    \end{bmatrix}
    \begin{bmatrix}
        x  \\ y \\ 1
    \end{bmatrix}=
    \begin{bmatrix}
        x+t_x \\ y+t_y \\ 1 
    \end{bmatrix} \\ \\
    向量平移：
    \begin{bmatrix}
        x^\prime \\ y^\prime \\ 0
    \end{bmatrix} = 
    \begin{bmatrix}
        1 & 0 & t_x \\
        0 & 1 & t_y \\
        0 & 0 & 1
    \end{bmatrix}
    \begin{bmatrix}
        x  \\ y \\ 0
    \end{bmatrix}=
    \begin{bmatrix}
        x \\ y \\ 0
    \end{bmatrix}
\end{matrix} 
$$

不难发现，向量的齐次坐标第三维设置为0可以保证向量的平移不变性。
>其余变换对应的仿射变换矩阵只需要在(3,3)处添加1即可，其余位置为0

### 3.3 组合变换

$$
\begin{matrix}
    \begin{bmatrix}
        x^\prime \\
        y^\prime \\
        z^\prime \\
        0 or 1
    \end{bmatrix} =
    \begin{bmatrix}
        1 & 0 & 0 &t_x \\
        0 & 1 & 0 &t_y \\
        0 & 0 & 1 &t_z \\
        0 & 0 & 0 & 1
    \end{bmatrix}
    \begin{bmatrix}
        a & b & c & 0 \\
        d & e & f & 0\\
        g & h & i & 0\\
        0 & 0 &0 &1
    \end{bmatrix}
    \begin{bmatrix}
        x\\y\\z\\0or1
    \end{bmatrix}
\end{matrix}
$$
>一般物体先线性变换，后平移变换

# 4. 视图变换(View transformation)
>让物体和摄像机做相反的变换，获得以摄像机为原点的空间坐标

$$
\begin{matrix}
    M_{view} = R_{view}T_{view} \\
    R_{view} = R_{camera}^{-1} = R_{camera}^T\\
    T_{view} = T_{camera}^{-1}
\end{matrix}
$$

# 5. 投影变换(Projection transformation)
>将三维坐标投影到二维
### 5.1 正交投影（Orthographic）
将矩形空间缩放到标准正方体中

$$
\begin{matrix}
    M_{ortho}=
    \begin{bmatrix}
        \frac{2}{l} & 0 & 0 & 0\\
        0 & \frac{2}{b} & 0 & 0 \\
        0 & 0 & \frac{2}{h} & 0 \\
        0 & 0 & 0 & 1
    \end{bmatrix}
\end{matrix}
$$
### 5.2 透视投影（Perspective projection）

<center><img alt=picture 0 src=../images/chapter1%20%E7%9F%A9%E9%98%B5%E4%B8%8E%E5%8F%98%E6%8D%A21748264356044.png width=400></center>
