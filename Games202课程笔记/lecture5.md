# PRT(Precomputed Radiance Transfer)

## 球谐函数

<center><img alt=图 0 src=../images/lecture51783946463259.png width=500></center>

- $l$ 频率，$m$ 编号。
- 蓝色代表负值，黄色代表正值。
- 这里的所有球谐函数都两两正交，且系数独立。

$$f(x) = \sum_i c_i \cdot B_i(x)$$
>使用球谐函数作为基函数对函数 $f$ 进行变换
$$c_i = \int_{\Omega} f(w) \cdot B_i(w) \, dw$$
>球谐函数系数计算
$$\hat{f}_L(\theta, \phi) = \sum_{l=0}^L \sum_{m=-l}^l c_{lm} \cdot B_{lm}(\theta, \phi)$$

>球谐函数近似的离散形态

<center><img alt=图 1 src=../images/lecture51783948366676.png></center>

>由图可以看出球谐函数可以保留大尺度的低频信息

## 光线贴图预计算

**计算Diffuse时使用前3阶球谐函数表示BRDF和光线贴图，然后根据方向进行采样后相乘。**

<center><img alt=图 2 src=../images/lecture51783948776394.png width=500></center>

- 场景静态时，可以将lighting、visibility、BRDF先点乘后再一起使用球谐函数表示。

<center><img alt=图 3 src=../images/lecture51783949677748.png width=500></center>

>使用不同阶球谐函数的表示情况

$$L_o(p, w_o) = \int_{\Omega^+} \underbrace{L_i(p, w_i)}_{Lighting} \underbrace{f_r(p ,w_i, w_o) \cos \theta_i V(p, w_i)}_{Light Transport} \, d w_i$$

$$L_o(p, w_o) = \sum_p \sum_q c_p c_q \int_{\Omega^+} B_p(w_i) B_q(w_i) \, d w_i$$

$$\sum_{i=1}^n [c_1^2,c_2^2,\dots ,c_n^2] \cdot \begin{bmatrix} B_1(w_i)^2 & 0 & \dots & 0 \\ 0 & B_2(w_i)^2 & \dots & 0  \\ \vdots & \vdots &\ddots & 0\\
0 & 0 & \ldots & B_n(w_i)^2 & \end{bmatrix}$$

>这里 $p \neq q$ 时，$B_p(w_i)B_q(w_i) = 0$

diffuse的物体不同 $w_o$ 都相同，只需要计算一次 $L_o(p, w_o)$ 即可。结果是一个 $n$ 维向量 $[c_1^2,c_2^2,\dots ,c_n^2]$。

glossy的物体不同 $w_o$ 都不同，需要计算 $L_o(p, w_o)$ 多次。因此结果是一个 $m\times n$ 的矩阵，$n$ 是球谐函数的阶，$m$ 是 $w_o$ 的方向数。

$$\begin{bmatrix} c_{1,1}^2 & \dots & c_{1,n}^2 \\ \vdots & \ddots & \vdots \\ c_{m,n}^2 & \dots & c_{m,n}^2 \end{bmatrix}$$

>Lighting部分不仅可以预计算单次弹射，还可以计算多次弹射。

## 贴图小波变换

<center><img alt=图 5 src=../images/lecture51785862326279.png ></center>

>使用小波变换对BRDF和光线贴图进行压缩。

<center><img alt=图 4 src=../images/lecture51785862312682.png ></center>

>SH压缩和小波变换压缩渲染效果对比

# RSM

# f 附录

## f1 小波变换

**Morlet 小波**

$$\Psi(x) =  \exp(-\frac{x^2}{2}) \cdot \cos(\omega x)$$

<center><img alt=图 0 src=../images/lecture51785854946354.png ></center>

$$\Psi_{a,b}(x) = a \exp(-\frac{(x-b)^2}{2}) \cdot \cos(\omega (x-b))$$

<center><img alt=图 3 src=../images/lecture51785855494130.png ></center>

>a=2,b=2的Morlet小波函数图

<center><img alt=图 1 src=../images/lecture51785855266334.png ></center>

>对一段信号进行Morlet小波变换结果，同时可以看到时域和频域的情况

- 小波变换虽然能同时保留时域和频域信息，但精度比不上时域信号和频域信号。频域效果完全比不上傅里叶变换。