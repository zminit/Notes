# 1. 采样(Sampling)
### 1.1 采样

扫描像素中心点坐标，判断是否在三角面片内部，中心点即为采样点

<center><img alt=图 0 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748333458531.png width=400></center>

判断方法：
<center><img alt=图 1 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748333720274.png width=400></center>

$$
\begin{matrix}
    \triangle ABC:\boldsymbol{AB}\times\boldsymbol{AP},\boldsymbol{BC}\times\boldsymbol{BP},\boldsymbol{CA}\times\boldsymbol{CP}方向相同时，P在\triangle ABC内 \\
    \boldsymbol{AB},\boldsymbol{BC},\boldsymbol{CA}首尾相接
\end{matrix}
$$

>边缘上的点处理方法比较灵活，OpenGL和DirectX将左边和上边定义在三角形内

一种较为优化的扫描方法：
<center><img alt=图 2 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748341578740.png width=400></center>


### 1.2 走样

<center>
<img alt=图 5 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748341863576.png width=200/>
<img alt=图 3 src=../images/chapter2%20%E5%85%89%E6%A0%85%E5%8C%961748341694812.png width=200/>
</center>