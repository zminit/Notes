# 实时阴影

## 渲染方程近似

$$
\int_{\Omega}f(x)g(x)\, dx \approx \frac{\int_{\Omega} f(x)\,dx}{\int_{\Omega}\,dx}\int_{\Omega}g(x)\,dx
$$

- $\Omega$ 足够小，该近似准确
- $g(x)$ 在 $\Omega$ 范围内变化不大（smooth，光滑，低频）,近似准确。

$$
L_0(p,\omega_0) = \int_{\Omega^+}L_i(p,\omega_i)f_r(p,\omega_i,\omega_o)\,\cos\theta_iV(p,\omega_i)\,d\omega_i
$$

$$
L_0(p,\omega_0) \approx
\underbrace{\frac{\int_{\Omega^+}V(p,\omega_i)\, d\omega_i}{\int_{\Omega^+}\,d\omega_i}}_{\text{visibility}}
\underbrace{\int_{\Omega^+}L_i(p,\omega_i)f_r(p,\omega_i,\omega_o)\,\cos\theta_i\,d\omega_i}_{\text{shading}}
$$

- 对点，方向光，visibility部分近似准确。
- 对`diffuse bsdf`,`constant radiance area lighting`,shading部分为smooth，该近似准确。
- **特别的**，BRDF非smooth，该近似不准确，因此不适合使用Shadow mapping。

## Shadow mapping

<center><img alt=图 1 src=../images/lecture31780133378352.png></center>

**shadow mapping原理**

- 在光源视角渲染一张纹理，保存场景中物体的深度或者距离信息。
- Shadow mapping 可以保存线性距离，也可以保存mvp转换后的z坐标
- 在摄像机视角渲染时，计算屏幕片元采样点到光源的距离，和对应的shadow map纹理单元作比较比较。
- 如果屏幕片元采样点p到光源的距离大于shadow map纹理单元保存的值，代表没有被遮挡，否则有阴影。

**缺点**

会出现条纹

如上图所示，shadow map中A到B的区域所有点到光源的距离被储存为同一值（如黄线），当摄像机观察点p时，真正的距离（红线）比黄线要长，错误地判断该点有阴影。

**解决方案**

- 增加bias

<center><img alt=图 3 src=../images/lecture31780199969528.png></center>

>在渲染屏幕时计算片元采样点到光源距离时减去 $bias$ ，如 $p$ 和 $p'$ ，可消除条纹，但是会出现阴影与物体分离的问题，如 $q$ 和 $q'$ 。 

**原理解析**

shadow mapping中，阴影计算就是渲染方程近似中的visibility部分，光源空间片元覆盖的场景区域越小，则准确度越高，也即，shadow map分辨率越高，准确度越高，条纹越细。


## PCF(Percentage Closer Filtering)

> PCF技术用于shadow mapping抗锯齿


<center><img alt=图 2 src=../images/lecture31780147044883.png></center>

**PCF原理**：

在shadow map上找到屏幕片元采样点对应的纹理单元，取周围位置的深度值（如图中取3x3的空间），如果深度大于采样点则为1，小于则为0，最后计算均值，得到该点的 $\text{visiblity}$ 。

## PCSS(Percentage Closer Soft Shadows)

<center><img alt=图 4 src=../images/lecture31780206178988.png></center>

> 当光源有大小/体积时，软阴影就会出现

软阴影区域大小计算公式为：
$$W_{penumbra} = \frac{(d_{receiver} - d_{blocker}) * W_{Light}}{d_{blocker}}$$

<center><img alt=图 8 src=../images/lecture31780211218831.png></center>

>根据 $W_{penumbra}$ 计算在shadow map上的采样分布半径r（正比于 $W_{penumbra}$ ）。
>例如上图，计算a、b、c三点在shadow map上的位置，在三点周围进行以r为半径进行泊松圆盘采样得到采样点深度，与a、b、c三点到光源中心距离进行比较，大于等于为1，小于为0（PCF），最后将均值作为阴影强度。

这里每个点使用的shadow map采样半径相同。

<center><img alt=图 6 src=../images/lecture31780206851229.png></center>

**具体过程**

- 以光源中心为观察视角生成shadow map。
- 在shadow map上计算一个blocker查找平面。
- 找到所有的blocker纹理单元（纹理值大于点p到光源的距离），计算均值作为 $d_{blocker}$。
- 计算 $W_{penumbra}$ 和shadow map采样半径。
- 以屏幕片元对应到shadow map的uv位置为中心进行采样。
- 计算阴影强度。
