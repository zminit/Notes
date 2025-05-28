# 1. 反射光

### 1.1 漫反射（Diffuse）
<center><img alt=图 1 src=../images/chapter3%20%E7%9D%80%E8%89%B21748421846227.png width=500></center>

>着色点漫反射强度和与光源的距离以及入射角有关，与观察者无关

$$
L_d = k_d(I/r^2)\max(0,\bold{n}\cdot\bold{l}) \\
$$
$$
\begin{align*}
    & L_d:光照强度 \\
    & k_d:反射系数 \\
    & I:距光源单位距离的光照强度 \\
    & r:着色点距光源距离 \\
    & \bold{n}:着色点法向量（单位向量） \\
    & \bold{l}:着色点入射光线（单位向量）
\end{align*}
$$

### 1.2 镜面反射（Specular）

<center><img alt=图 2 src=../images/chapter3%20%E7%9D%80%E8%89%B21748423125369.png width=500></center>

$$
\begin{matrix}
   L_s = k_s(I/r^2)\max(0,\cos\theta)^p = k_s(I/r^2)\max(0,\bold{n}\cdot\bold{h})^p \\
   \bold{h} = bisector(\bold{v},\bold{l}) = \frac{\bold{v} + \bold{l}}{\lVert\bold{v}+\bold{l}\rVert} 
\end{matrix}
$$
$$
\begin{align*}
    & L_s:反射光强度 \\
    & k_s:反射系数 \\
    & \bold{h}:半程向量:(观察角度+入射角度) /2 \\
    & \bold{v}:观察向量
\end{align*}
$$

### 1.3 环境光（Ambient）

>简化情况下：假设环境光强度是一个常数

$$
L_a = k_aI_a
$$

### 1.4 Blinn-Phong 反射模型

$$
L = L_d + L_s + L_a
$$

Blinn-Phong模型：
- 简化环境光
- 不考虑观察者距离衰减



# 2. 着色频率（Shading Frequencies）
 
<center><img alt=图 3 src=../images/chapter3%20%E7%9D%80%E8%89%B21748430638959.png width=500></center>

### 2.1 逐片元着色（Flat Shading）
>以片元为单位着色

### 2.2 逐顶点着色（Gouraud Shading）
>以顶点为单位着色

$$
顶点法线：N_v = \frac{\sum_i N_i}{\lVert\sum_i N_i\rVert}
$$

### 2.3 逐像素着色（Phong Shading）
>以像素为单位着色

# 3. 渲染管线
<center><img alt=图 4 src=../images/chapter3%20%E7%9D%80%E8%89%B21748431471203.png width=500></center>

深度测试：Fragment Processing

着色：Vertex Processing / Fragment Processing


# 4. 纹理映射（Texture Mapping）
