# 1. 反射光

### 1.1 漫反射（Diffuse）
<center><img alt=图 1 src=../images/chapter3%20%E7%9D%80%E8%89%B21748421846227.png width=500></center>

>着色点漫反射强度和与光源的距离以及入射角有关，与观察者无关

$$
L_d = k_d(I/r^2)\max(0,\boldsymbol{n}\cdot\boldsymbol{l}) \\
$$
$$
\begin{align*}
    & L_d:光照强度 \\
    & k_d:反射系数 \\
    & I:距光源单位距离的光照强度 \\
    & r:着色点距光源距离 \\
    & \boldsymbol{n}:着色点法向量（单位向量） \\
    & \boldsymbol{l}:着色点入射光线（单位向量）
\end{align*}
$$

### 1.2 镜面反射（Specular）

<center><img alt=图 2 src=../images/chapter3%20%E7%9D%80%E8%89%B21748423125369.png width=500></center>

$$
\begin{matrix}
   L_s = k_s(I/r^2)\max(0,\cos\theta)^p = k_s(I/r^2)\max(0,\boldsymbol{n}\cdot\boldsymbol{h})^p \\
   \boldsymbol{h} = bisector(\boldsymbol{v},\boldsymbol{l}) = \frac{\boldsymbol{v} + \boldsymbol{l}}{\lVert\boldsymbol{v}+\boldsymbol{l}\rVert} 
\end{matrix}
$$
$$
\begin{align*}
    & L_s:反射光强度 \\
    & k_s:反射系数 \\
    & \boldsymbol{h}:半程向量:(观察角度+入射角度) /2 \\
    & \boldsymbol{v}:观察向量
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

### 4.1 重心插值
>逐顶点着色中处理三角形中间的着色问题

<center><img alt=图 5 src=../images/chapter3%20%E7%9D%80%E8%89%B21748507808637.png width=500></center>

>与三角形共面的点坐标都可以表示为三个顶点的线性组合
>
>**特别的**：当线性组合系数非负时，该点一定在三角形内


**重心坐标**： $点D与\triangle ABC共面，D表示为D = \alpha A + \beta B + \gamma C, 则D对应的\boldsymbol{重心坐标}即(\alpha,\beta,\gamma)$

<center><img alt=图 6 src=../images/chapter3%20%E7%9D%80%E8%89%B21748508492433.png width=500></center>

>可以通过计算三角形的面积比计算重心坐标，三角形面积等于边向量叉乘模/2

```mermaid
graph LR
    A[坐标]--->B[重心坐标]--->C[插值]
```

$$
V_D = \alpha V_A + \beta V_B + \gamma V_C
$$

### 4.2 双线性插值

>像素精度比纹理精度高时，解决走样的问题

<center><img alt=图 7 src=../images/chapter3%20%E7%9D%80%E8%89%B21748509749288.png></center>

红点为像素点(Pixel)，方框为纹理元素(Texttel)

### 4.3 Mipmap
>解决纹理精度高于像素精度导致的走样问题，快速、不准确、方形的区域查询

1. 纹理图像预处理：
<center><img alt=picture 2 src=../images/chapter3%20%E7%9D%80%E8%89%B21749137747700.png width=400></center>

<center><img alt=picture 1 src=../images/chapter3%20%E7%9D%80%E8%89%B21749137722013.png width=500></center>

2. 计算层数
<center><img alt=picture 0 src=../images/chapter3%20%E7%9D%80%E8%89%B21749137665704.png width=500></center>

3. 三线性插值

>对于层数非整数的结果在邻近两层进行插值后再进行一次插值
<center><img alt=picture 3 src=../images/chapter3%20%E7%9D%80%E8%89%B21749137900164.png width=500></center>

### 4.4 其他纹理

**环境光映射**
<center><img alt=图 4 src=../images/chapter3%20%E7%9D%80%E8%89%B21750004201714.png ></center>
环境光贴图：将环境光信息作为纹理

<center><img alt=图 5 src=../images/chapter3%20%E7%9D%80%E8%89%B21750004300798.png ></center>
立方体映射：将环境光信息存在立方体表面

**凹凸纹理**

<center><img alt=图 6 src=../images/chapter3%20%E7%9D%80%E8%89%B21750004530252.png ></center>
法线贴图：在不改变模型的情况下改变模型表面的法线
<center><img alt=图 7 src=../images/chapter3%20%E7%9D%80%E8%89%B21750004582782.png ></center>

>三维法线贴图法线计算方法

**位移贴图**
<center><img alt=图 8 src=../images/chapter3%20%E7%9D%80%E8%89%B21750004657239.png ></center>

左：法线贴图，右：位移贴图

位移贴图：改变模型顶点位置实现