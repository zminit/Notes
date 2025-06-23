# 1. 反射

### 1.1 漫反射系数

>BRDF函数值即为物体的材质反射数据，一般为 $f_r$

<center><img alt=图 0 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750668168449.png width=400></center>

$此时假设漫反射各个方向光线相同，即L_i=L_o(w_o)=C$

### 1.2 反射定律

<center><img alt=图 1 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750668847192.png width=400></center>

这里入射和出射光线方向向量和法线向量均为单位向量

### 1.3 菲涅尔像

不同角度射入的关系反射的能量不相同

<center><img alt=图 5 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750669990842.png width=400></center>

<center><img alt=图 6 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750670159523.png width=400></center>

>绝缘体和导体光线入射角与反射能量直接的关系（垂直照射反射能量最少）

<center><img alt=图 7 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750670329014.png width></center>

>菲涅尔像准确计算公式和简化近似公式，R0为0度时的反射率，n为折射率

# 2. 折射

### 2.1 斯涅尔定律

<center><img alt=图 2 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750669098726.png width=400></center>

$$
\eta_i\sin\theta_i = \eta_t\sin\theta_t,\eta为折射率
$$

<center><img alt=图 3 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750669380103.png width=400></center>

在某些情况下折射不会发生，只有反射

<center><img alt=图 4 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750669523305.png width=400></center>

# 3. 微表面模型


### 3.1 法线分布
<center><img alt=图 8 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750670574201.png width=400></center>

<center><img alt=图 9 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750670622701.png width=400></center>

>微表面模型计算反射, F为菲涅尔像计算函数，D为法线分布函数， G为几何像

几何像：描述微表面自遮挡情况

### 3.2 各向异性

<center><img alt=图 10 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750671681223.png width=400></center>

# 4. BRDF

BRDF描述材质反射性质，有如下性质：
1. 非负性：BRDF值非负
<center><img alt=图 12 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750671889054.png width=300></center>
2. 线性性（可加性）：
<center><img alt=图 11 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750671870758.png width=400></center>
3. 可逆性：
<center><img alt=图 13 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750671918514.png width=400></center>
4. 能量守恒：
<center><img alt=图 14 src=../images/chapter6%20%E6%9D%90%E8%B4%A81750671954898.png width=400></center>