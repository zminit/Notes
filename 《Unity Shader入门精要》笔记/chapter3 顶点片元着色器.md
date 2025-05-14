# 1. 顶点/片元着色器
### 1.1 样例
```shaderlab
Shader "MyShader/SimpleShader"{
    SubShader {
        Pass {
            CGPROGRAM //开始CG/HLSL代码

            #pragma vertex vert //顶点着色器函数名vert
            #pragma fragment frag //片元着色器函数名frag

            float4 vert(float4 v : POSITION) : SV_POSITION {
                return mul(UNITY_MATRIX_MVP, v);
            }
            //输入float4类型的坐标，输出裁剪坐标

            fixed4 frag() : SV_Target{
                return fixed4(1.0, 1.0, 1.0, 1.0);
            }
            //输出白色到渲染目标

            ENDCG
        }
    }
}
```

CG/HLSL函数格式：
```shaderlab
返回类型 函数名(类型 参数 ： 输入语义) ： 输出语义{
    ...
}
```
### 1.2 Unity语义
- **POSITION**
- **TANGENT**
- **NORMAL**
- **TEXCOORD0**
- **TEXCOORD1**
- **TEXCOORD2**
- **TEXCOORD3**
- **TEXCOORD4**
- **COLOR**
