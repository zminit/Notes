# 1. 漫反射shader

## 1.1 标准光照模型

>**标准光照模型**：只关注直接光照，不考虑多次反射进入摄像机的光线
>
>**兰伯特定律**：如下的漫反射计算公式
>
>**Phong 着色** : 逐像素计算光照
>
>**Gouraud 着色** : 逐顶点计算光照

计算物体光照一般分为四个部分:

$$
\begin{align*}
    &1. 自发光 c_{emissive}=m_{emissive} \\
    &2. 高光 c_{specular} = (c_{light} * m_{specular})\max(0, \bold{v}\cdot\bold{r})^{m_{gloss}} = (c_{light} * m_{specular})\max(0, \bold{n}\cdot\bold{h})^{m_{gloss}} \\
    &3. 漫反射 c_{diffuse} = (c_{light} * m_{diffuse})\max(0, \bold{n} \cdot \bold{I} ) \\
    &4. 环境光 c_{ambient} \\ \\
    & c_{light}:光源到物体表面的光线 \\
    & m_{specular} : 高光反射颜色 \\
    & m_{gloss} : 光泽度 \\
    & m_{diffuse} : 漫反射系数 \\
    & \bold{v} : 视线（指向视线源） \\
    & \bold{r} : 反射光线 \\
    & \bold{n} : 反射面法线 \\
    & \bold{h} : 半程向量 = \frac{\bold{v}+\bold{i}}{|\bold{v}+\bold{i}|} \\
    & \bold{I} : 入射光线
\end{align*}
$$

### 1.2 Blinn-Phong模型shader


#### 1.2.1 逐顶点计算diffuse
```shaderlab
Shader "Diffuse Vertex-Level"{
    Properties{
        _Diffuse ("Diffuse", Color) = (1, 1, 1, 1) //漫反射颜色
    }

    SubShader{
        Pass{
            Tags { "LightMode" = "ForwardBase"} //Unity独有

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "Lighting.cginc"

            fixed4 _Diffuse;

            struct a2v{
                float4 vertex : POSITION; //模型空间顶点坐标
                float3 normal : NORMAL; //模型空间法线向量
            };

            struct v2f{
                float4 pos : SV_POSITION; //用于表示渲染坐标
                fixed3 color : COLOR;
                float3 worldNormal : TEXCOORD0; 
            };

            v2f vert(a2v v) {
                v2f o;
                o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
                fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
                float3 worldNormal = normalize(mul(unity_WorldToObject, v.normal));
                float3 worldLight = normalize(_WorldSpaceLightPos0.xyz);
                fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * saturate(dot(worldNormal, worldLight));
                o.color = ambient + diffuse;
                return o;
            }

            fixed4 frag(v2f i) : SV_Target{
                return fixed4(i.color, 1);
            }

            ENDCG
        }
    }
    Fallback "Diffuse"
}
```
1. `Tags`是渲染引擎进行的封装，底层api如DirectX并不支持，不同引擎支持的tags不一样，比如`LightMode`就是Unity独有的
2. 结构体中的语义指示了变量储存的数据类型，GPU会根据语义读写变量，比如`a2v`类型的数据在传入`vert`时就会被GPU赋值，其中vertex会赋位置信息， `v2f`中的`pos`会在渲染时被作为渲染目标坐标读取
3. 在Properties中声明过的全局变量能够在inspector中修改数据
4. `worldNormal`的计算有些反直觉，因为法线的坐标变换比较特殊，经过简单的推导发现，切线向量或者单纯的点坐标从模型空间变换到世界空间时只需要乘以`unity_ObjectToWorld`，但法线需要乘以这个矩阵的逆转置矩阵，即`unity_WorldToObject`


#### 1.2.2 逐像素漫反射
```shaderlab
Shader "Diffues Pixel-Level"{
    Properties{
        _Diffuse ("Diffuse", Color) = (1, 1, 1, 1)
    }

    SubShader{
        Pass{
            Tags {"LightMode" = "ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "Lighting.cginc"

            fixed4 _Diffuse;

            struct a2v{
                float4 vertex : POSITION;
                float3 normal : NORMAL;
            };

            struct v2f{
                float4 pos : SV_POSITION;
                float3 worldNormal : TEXCOORD0;
            };

            v2f vert(a2v v){
                v2f o;
                o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
                o.worldNormal = normalize(mul(unity_WorldToObject, v.normal));
                return o;
            }

            fixed4 frag(v2f i) : SV_Target{
                fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
                float3 worldLight = normalize(_WorldSpaceLight0.xyz);
                fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * saturate(dot(i.worldNormal, worldLight));
                return fixed4(ambient+diffuse, 1);
            }
            ENDCG
        }
    }
    FallBace "Diffuse"
}
```

#### 1.2.3 逐顶点计算高光
```shaderlab
Shader "Specular Vertex-Level"{
    Properties{
        _Diffuse ("Diffuse", Color) = (1, 1, 1, 1)
        _Specular ("Specular", Color) = (1, 1, 1, 1)
        _Gloss ("Gloss", Range(8.0, 256)) = 80
    }

    SubShader{
        Pass{
            Tags {"LightMode"="ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "Lighting.cginc"

            fixed4 _Diffuse;
            fixed4 _Specular;
            float _Gloss;

            struct a2v{
                float4 vertex : POSITION;
                float3 normal : NORMAL;
            };

            struct v2f{
                float4 pos : SV_POSTIION;
                fixed3 color : COLOR;
            };

            v2f vert(a2v v){
                v2f o;
                o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
                float3 worldNormal = normalize(mul(unity_WorldToObject, v.normal));
                fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
                float3 worldLight = normalize(_WorldSpaceLight0.xyz);
                fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * saturate(dot(worldLight, worldNormal));
                float4 worldPos = mul(unity_ObjectToWorld, v.vertex);
                float3 viewDir = normalize(WorldSpaceViewDir(worldPos));
                float3 halfDir = normalize(viewDir, worldLight);
                fixed3 specular = _LightColo0.rgb * _Specular.rgb * pow(saturate(halfDir, worldNormal), _Gloss);
                o.color = diffuse + ambient + specular;
                return o;
            }

            fixed4 frag(v2f i) : SV_Target{
                return fixed4(i.color, 1);
            }

            ENDCG
        }
    }
    FallBack "Diffuse"
}

```

#### 1.2.4 逐像素计算高光

```shaderlab
Shader "Specular Pixel-Level"{
    Properties{
        _Diffuse ("Diffuse", Color) = (1, 1, 1, 1)
        _Specular ("Specular", Color) = (1, 1, 1, 1)
        _Gloss ("Gloss", Range(8.0, 256)) = 80
    }

    SubShader{
        Pass{
            Tags {"LightMode"="ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "Lighting.cginc"

            fixed4 _Diffuse;
            fixed4 _Specular;
            float _Gloss;

            struct a2v{
                float4 vertex : POSITION;
                float3 normal : NORMAL;
            };

            struct v2f{
                float4 pos : SV_POSTIION;
                float3 worldPos : TEXCOORD1;
                float3 worldNormal : TEXCOORD0;
            };

            v2f vert(a2v v){
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldNormal = normalize(mul(v.normal, (float3x3)unity_WorldToObject));
                o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
                return o;
            }

            fixed4 frag(v2f i) : SV_Target{
                fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
                float3 worldLight = normalize(_WorldSpaceLightPos0.xyz);
                fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * saturate(dot(i.worldNormal, worldLight));
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));
                float3 halfDir = normalize(viewDir + worldLight);
                fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(saturate(dot(i.worldNormal, halfDir)), _Gloss);
                return fixed4(specular + ambient + diffuse, 1);
            }

            ENDCG
        }
    }
    FallBack "Diffuse"
}

```
1. **shader中将向量储存为行向量**，所以和矩阵相乘时是向量×矩阵，而**坐标被储存为列向量**，因此坐标变换时是变换矩阵×坐标
2. WorldSpaceViewDir(float4`模型空间坐标`) ，UnityWorldSpaceViewDir(float3`世界空间坐标`)

