# 1. 渲染队列

|队列名|索引号|用途|
|:---:|:---:|:---:|
|Background|1000|一般用于渲染背景物体。|
|Geometry|2000|默认，一般用于不透明物体。|
|AlphaTest|2450|用于透明测试的物体（测试不通过舍弃片元）,在Unity 5中单独分出|
|Transparent|3000|用于透明度混合，从后往前渲染|
|Overlay|4000|一般用于实现叠加效果，最后渲染|

```shaderLab
SubShader{
    Tags {"Queue"="AlphaTest" "IgnoreProjector"="True" "RenderType"="TransparentCutout"}
    Pass{
        Tags {"LightMode"="ForwardBase"}
        CGPROGRAM

        #pragma vertex vert
        #pragma fragment frag

        #include "Lighting.cginc"

        fixed4 _Color;
        sampler2D _MainTex;
        float4 _MainTex_ST;
        fixed _Cutoff;
    }
}
```