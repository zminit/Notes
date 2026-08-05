# 1. 渲染路径

Unity有三种渲染路径：**前向渲染**，**延迟渲染**，**顶点照明**

渲染路径一般在`Pass`或者`Subshader`中
```shaderlab
Tags {"LightMode"="Forwardbase"}
```

**前向渲染**：
1. **forwardbase**:一般处理最亮的平行光和光线顶点着色
2. **forwardadd**:一般用于聚光灯，点光源等光源进行片元着色

**延迟渲染**：
一般用于处理多个光源重叠空间的渲染，不对每个光源执行pass,使用G缓冲后只执行一次pass。

## 1.1 前向渲染
前向渲染有两种Pass：**ForwardBase**, **ForwardAdd**

1. Base Pass无论有多少光源，只执行一次，**主光源**和**非重要光源**就在BasePass中渲染。
2. Add Pass会为每一个除主光源外的逐像素处理的光源执行一次。

# 2. 复杂光照

## 2.1 不同光照处理

1. 最亮的平行光或某一个其他光源在BasePass中按逐像素进行渲染，其他光源如非重要光源、SH球谐光会在BasePass中按照逐顶点方式渲染。
   - unity选取主光源顺序：**最亮平行光** > **最近其他光源**，在unity有关于光源评分的机制，评分最高的选为主光源，平行光优先级大于其他光源。
2. 除了主光源的其他重要光源在forwardadd Pass中逐像素渲染。
3. 非重要光源会按照SH光方式，渲染进 **UNITY_LIGHTMODEL_AMBIENT** 变量中。
4. 设置为**important**的光源一定会按照逐像素的方式渲染。
5. unity最多会设置n个光源逐像素渲染，n为Edit -> Project Settings -> Quality中pixel light count的值。如果import光源大于n，所有auto的光源会按非重要光源渲染。

<center><img alt=图 0 src=../images/chpater7%20%E5%A4%8D%E6%9D%82%E5%85%89%E7%85%A71763214881108.png ></center>

>帧调试器（frameDebugger）
>
>Window -> Analysis -> Frame Debugger

## 2.2 光照纹理

点光源和聚光灯计算光线衰减公式计算效率低，unity采用对光照衰减纹理进行采样进行优化。

```GLSL
    fixed3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
    float3 lightCoord = mul(unity_WorldToLight, float4(i.worldPos, 1)).xyz;
    fixed atten = tex2D(_LightTexture0, dot(lightCoord, lightCoord).rr).UNITY_ATTEN_CHANNEL;
```
**_LightTexture0**: 光照衰减纹理。

# 3. 阴影

<center><img alt=图 2 src=../images/chpater7%20%E5%A4%8D%E6%9D%82%E5%85%89%E7%85%A71763222162613.png ></center>

## 3.1 ShadowMap
阴影映射（ShadowMap）是光源视角下的深度图像

1. 平行光ShadowMap

<center><img alt=图 1 src=../images/chpater7%20%E5%A4%8D%E6%9D%82%E5%85%89%E7%85%A71763222078908.png ></center>

>平行光的级联贴图（从左到右，从下到上）

<center><img alt=图 3 src=../images/chpater7%20%E5%A4%8D%E6%9D%82%E5%85%89%E7%85%A71763222247676.png ></center>

>平行光阴影贴图绘制顺序

2. 屏幕空间ShadowMap
<center><img alt=图 4 src=../images/chpater7%20%E5%A4%8D%E6%9D%82%E5%85%89%E7%85%A71763355894926.png ></center>

>经过实验发现，屏幕空间的阴影映射（Screenspace Shadowmap）只有在场景中有平行光的时候才会生成（Draw GL事件）。可能是只有在BasePase中逐像素渲染光源时才会用到。

3. 点光源ShadowMap

<center><img alt=图 5 src=../images/chpater7%20%E5%A4%8D%E6%9D%82%E5%85%89%E7%85%A71763356630782.png ></center>

<center><img alt=图 7 src=../images/chpater7%20%E5%A4%8D%E6%9D%82%E5%85%89%E7%85%A71763356823464.png width=300></center>

>点光源会在一个cubemap上生成6张ShadowMap，这里节选一张带capsule的。

4. 聚光灯ShadowMap

<center><img alt=图 8 src=../images/chpater7%20%E5%A4%8D%E6%9D%82%E5%85%89%E7%85%A71763356961597.png width=400></center>

>聚光灯斜向下俯视Capsule


## 3.1 投影和接收阴影

投下阴影需要ShadowCaster Pass
```GLSL
Pass{
    Tags {"LightMode" = "ShadowCaster"}

    CGPROGRAM
    #pragma multi_compile_shadowcaster
    #pragma vertex vert
    #pragma fragment frag
    #include "UnityCG.cginc"

    struct v2f{
        V2F_SHADOW_CASTER;
    };

    v2f vert( appdata_base v){
        v2f o;
        TRANSFER_SHADOW_CASTER_NORMALOFFSET(o)
        return o;
    }

    float4 frag(v2f i):SV_Target
    {
        SHADOW_CASTER_FRAGMENT(i)
    }
    ENDCG
}
```
接收阴影需要在BasePass中加入
1. **SHADOW_COORDS**：阴影纹理采样结果写入寄存器。
2. **TRANSFER_SHADOW**：阴影采样。
3. **UNITY_LIGHT_ATTENUATION**：获取阴影和光线衰减叠加后的衰减系数。

```GLSL
struct v2f{
    ...
    SHADOW_COORDS(2);//2为寄存器编号，如0，1，2...
};

v2f vert(a2v v){
    v2f o;
    ...
    TRANSFER_SHADOW(o);
}

fixed4 frag(v2f i) : SV_Target{
    ...
    UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos);
}
```
物体Mesh Renderer处可以设置阴影接受配置

<center><img alt=图 9 src=../images/chpater7%20%E5%A4%8D%E6%9D%82%E5%85%89%E7%85%A71763357157776.png ></center>