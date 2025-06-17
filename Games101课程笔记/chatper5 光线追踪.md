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

4. **包围盒求交**

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

     