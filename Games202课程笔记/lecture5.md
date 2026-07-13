# PRT(Precomputed Radiance Transfer)

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

**计算Diffuse时使用前3阶球谐函数表示BRDF和光线贴图，然后根据方向进行采样后相乘。**

<center><img alt=图 2 src=../images/lecture51783948776394.png width=500></center>

- 场景静态时，可以将lighting、visibility、BRDF先点乘后再一起使用球谐函数表示。

<center><img alt=图 3 src=../images/lecture51783949677748.png width=500></center>

>使用不同阶球谐函数的表示情况
