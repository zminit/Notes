# 1. 几何
几何体表示有两种，一种是隐式几何，一种是显式几何对应着隐式函数和显式函数

显式表示：直接定义/参数表示

隐式表示：

# 2. 曲线

### 2.1 贝塞尔曲线
<center><img alt=图 0 src=../images/chapter4%20%E5%87%A0%E4%BD%951750008725063.png width=400></center>
有n+1个控制点的称为n次贝塞尔曲线

**贝塞尔曲线计算**：
<center><img alt=图 1 src=../images/chapter4%20%E5%87%A0%E4%BD%951750009285837.png width=400></center>
对于每条线段上的点进行线性插值得到新线段，再对新线段端点线性插值得到最终结果

<center><img alt=图 2 src=../images/chapter4%20%E5%87%A0%E4%BD%951750009532180.png ></center>
<center><img alt=图 3 src=../images/chapter4%20%E5%87%A0%E4%BD%951750009758661.png ></center>
对给出的多条线段在t时刻进行线性插值后得到新的线段集，对新的线段集进行线性插值，最后得到最终t时刻点位置

<center><img alt=图 4 src=../images/chapter4%20%E5%87%A0%E4%BD%951750010044997.png width=400></center>
<center><img alt=图 5 src=../images/chapter4%20%E5%87%A0%E4%BD%951750010189408.png width=400></center>

>n+1个控制点对应的贝塞尔曲线点计算公式, $t\in (0,1), (^{n}_{i})=C^{i}_{n}$

**贝塞尔曲线的性质**：
1. 贝塞尔曲线的端点一定是控制点
2. 贝塞尔曲线具有仿射不变性
3. 贝塞尔曲线点不会超出控制点凸包的范围
4. 4个控制点的贝塞尔曲线： $b^\prime(0)=3(b_1-b_0),b^\prime(1)=3(b_3-b_2)$

# 3. 曲面
### 3.1 贝塞尔曲面
贝塞尔曲面是由多条贝塞尔曲线上的点再次进行贝塞尔计算得到

1. 先画出一个维度上的所有曲线
<center><img alt=图 6 src=../images/chapter4%20%E5%87%A0%E4%BD%951750012361238.png ></center>

2. 根据不同曲线同一个时间t的点计算第二个维度的贝塞尔曲线
<center><img alt=图 7 src=../images/chapter4%20%E5%87%A0%E4%BD%951750012452393.png ></center>

### 3.2 曲面细分

1. **Loop细分**

>生成新点
<center><img alt=图 0 src=../images/chapter4%20%E5%87%A0%E4%BD%951750064152561.png width=400></center>

>旧点位移
<center><img alt=图 1 src=../images/chapter4%20%E5%87%A0%E4%BD%951750064224077.png width=400></center>

2. **Catmull-Clark细分**

>生成中心点,
>在网格中心生成中心点

奇异点：度非4的点



<center><img alt=图 2 src=../images/chapter4%20%E5%87%A0%E4%BD%951750079410498.png width=400></center>

>连接中心点与临近的边中心点
<center><img alt=图 3 src=../images/chapter4%20%E5%87%A0%E4%BD%951750080906849.png width=400></center>

>改变各点位置

<center><img alt=图 4 src=../images/chapter4%20%E5%87%A0%E4%BD%951750081196804.png width=400></center>

**Catmull-Clark细分性质**：
1. 经过一次细分后奇异点数量不变，即一次细分后网格只剩四边形

### 3.3 曲面简化

**边坍缩算法**
<center><img alt=图 5 src=../images/chapter4%20%E5%87%A0%E4%BD%951750082141685.png width=400></center>

通过将一些边端点聚合到一起实现，难点在于选择坍缩的边

**二次误差测量**
<center><img alt=图 6 src=../images/chapter4%20%E5%87%A0%E4%BD%951750082232296.png width=400></center>

>计算坍缩后的顶点到被坍缩面的平方距离和，即为该次坍缩的**二次误差**

选择坍缩的边可以通过堆来计算

通过局部求最优解来进行解决整个模型的简化
