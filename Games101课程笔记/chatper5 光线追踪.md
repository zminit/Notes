# 1. Shadow Mapping

在光源处添加虚拟摄像机，分别比对**摄像机**和**虚拟摄像机**生成的**深度图**，匹配的地方即为物体，不匹配的即为阴影，即“光和眼睛都能看到的地方才有颜色”

<center><img alt=图 0 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750147272997.png width=400></center>

>Shadow Mapping只能生成硬阴影

# 2. 光线追踪

### 2.1 光线追踪
从摄像机发射射线，计算折射、反射到达物体表面的能量，同时计算光源是否对该点可见，最终得到该处的光线信息

<center><img alt=图 1 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750158820164.png></center>

### 2.2 交点计算

>可以将光线表示为 $r(t)=\boldsymbol{o}+t\boldsymbol{d},t\in(0,+\infty)$ 
>
>o为原点坐标
>
>d为光线方向向量


1. **计算物体表面函数与光线的交点**
    
    物体： $p:f(p)=0,p为空间中的点$
    
    交点方程：$f(o+td)=0$

2. **光线与平面求交**
    
    平面： $p:(p-p^\prime)\cdot N = 0 \to ax+by+cz+d=0$ 

    N：平面法线

    p：空间中的点

    $$
    t= \frac{(p^\prime-o)\cdot N}{d\cdot N}\enspace \boldsymbol{Check:}t\in [0,\infty)
    $$
    
3. **光线和三角形求交**

    <center><img alt=图 2 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750159594960.png width=400></center>
    
    通过三角形重心坐标的性质构造线性方程组求解

    和三角形共面的点的重心坐标非负，同时在三角形内的点重心坐标和为1

4. **包围盒求交（AABBs）**

    为了简化计算，使用**轴对齐立方体包围盒**代替物体进行计算

    每次计算光线与包围盒的两个无限大的对面的交点，连接两个交点，最后求多条线段的交集就是光在包围盒停留的时间。

    <center><img alt=图 3 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750160115271.png width=500></center>

    >上图演示二维包围盒求交计算

    对三维包围盒： $t_{enter}=\max\{t_{min}\}, t_{exit}=\min\{t_{max}\}$

    $t_{exit} > t_{enter} \And\And t_{exit} >=0 \iff$  光线与包围盒有交点 

    $t_{exit} < 0$ 时光源在包围盒内

    <center><img alt=图 4 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750161921958.png width=500></center>

    >上：光线与任意平面求交
    >
    >下：光线与包围盒对面求交（垂直于x轴）

### 2.3 包围盒内部处理

1. **网格化包围盒**
    
    1. 预处理：将包围盒均匀划分为小包围盒，将物体表面所在的小包围盒标记
    <center><img alt=图 0 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750254835596.png width=400></center>

    2. 计算光路：计算光会经过的包围盒，以及计算包围盒是否为物体表面
    <center><img alt=图 1 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750254913968.png width=400></center>

    >栅格法适合均匀分布的物体

2. **空间划分**
    <center><img alt=图 2 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750255131522.png width=400></center>
    
    空间划分有多种方法：八叉树、KD树、BSP树
    
    八叉树：每次递归将一个包围盒分为2^n个子包围盒，n为空间维度

    KD树：每次递归将包围盒沿轴向分为两份

    BSP树：每次递归将包围盒沿特定方向分为两份


    **KD-Tree**:
    <center><img alt=图 3 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750255430231.png  width=400></center>

    1. 将大包围盒分为递归分为两部分，知道某一部分符合特定条件为止（如：最多有n个三角形）
    2. 在叶子节点储存物体或三角形
    3. 计算光路与节点包围盒相交的情况，如果是非叶子节点则继续计算子节点，若是叶子节点，则相交时叶子节点包围盒内物体均与光线相交
    
    >空间划分会导致一个物体在两个划分中的问题

### 2.4 物体划分

<center><img alt=图 4 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750263317166.png width=400></center>

>**BVH**:递归将物体分为两堆，求包围盒

# 3. 辐射度量学

基础概念：
- **Radiant Flux**
    <center><img alt=图 5 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750263969691.png width=400></center>

    >单位时间内辐射的光子数,单位：流明

- **Radiant Intensity**
    <center><img alt=图 8 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750269043774.png width=400></center>

    >特定方向上的光线强度
    
    **Radiant Intensity**:
    
    <center><img alt=图 9 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750269940054.png width=500></center>
    
    >辐射能量/单位立体角
    
    **立体角：**
    <center><img alt=图 10 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750270010477.png width=400></center>
        
        弧度=弧长/半径

        立体角度=面积/半径^2

    <center><img alt=图 11 src=../images/chatper5%20%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA1750270156204.png width=400></center>
    
    >立体角微分

    **Irradiance**:接受量
    


    **Radiance**:辐射




    