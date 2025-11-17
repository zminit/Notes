# 1.  单张纹理

<center><img alt=图 0 src=../images/chapter5%20%E7%BA%B9%E7%90%86%E8%B4%B4%E5%9B%BE1757178339977.png ></center>

<center><img alt=图 1 src=../images/chapter5%20%E7%BA%B9%E7%90%86%E8%B4%B4%E5%9B%BE1757179348734.png ></center>

```shaderlab
Shader "Single Texture"{
    Properties{
        _Specular("Specular", Color) = (1,1,1,1)
        _MainTex("Main Texture", 2D) = "white" {}
        _Color("Color", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(8.0, 256)) = 20
    }

    SubShader{
        Pass{
            Tags {"LightMode" = "ForwardBase"}

            CGPROGRAM

            #pragma vertex vert
            #pragma fragment frag
            #include "Lighting.cginc"

            fixed4 _Specular;
            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _Color;
            float _Gloss;

            struct a2v{
                float4 vertex : POSITION;//齐次坐标
                float3 normal : NORMAL;//单位向量
                float4 texcoord : TEXCOORD;//纹理数据，包括缩放z，平移w
            }

            struct v2f{
                float4 pos : SV_POSITION;;
                float3 worldNormal : TEXCOORD0;
                float3 worldPos : TEXCOORD1;
                float2 uv : TEXCOORD2;
            }

            v2f vert(a2v v){
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.normal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld,v.vertex).xyz;
                o.uv = v.texcoord.xy * _MainTex_ST.xy + _MainTex_ST.zw;
                return o;
            }

            fixed4 frag(v2f i) : SV_Target{
                fixed3 albedo = tex2D(_MainTex, i.uv);
                fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo;//环境光
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));//入射光
                float3 worldNormal = normalize(i.worldNormal);// 法线
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));
                float3 halfDir = normalize(lightDir + viewDir);
                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, worldNormal));
                fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(halfDir, worldNormal)), _Gloss);
                return fixed4(ambient + specular + diffuse, 1.0);
            }
            ENDCG
        }
    }
    FallBack "Diffuse"
}
```

# 2. 凹凸纹理

<center><img alt=图 2 src=../images/chapter5%20%E7%BA%B9%E7%90%86%E8%B4%B4%E5%9B%BE1757179389110.png width=200></center>

>上图为法线纹理贴图效果。

```shaderlab
Shader "Normal Map In Tangent Space"{
    Properties{
        _Color("Color", Color) = (1,1,1,1)
        _MainTex("Main Texture", 2D) = "white" {}
        _BumpTex("Bump Texture", 2D) = "white" {}
        _BumpScale("Bump Scale", float) = 2.0
        _Specular("Specular", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(8.0, 256)) = 20
    }

    SubShader{
        Pass{
            Tags {"LightMode" = "ForwardBase"}

            CGPROGRAM

            #pragma vertex vert
            #pragma fragment frag
            #include "Lighting.cginc"

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _BumpTex;
            float4 _BumpTex_ST;
            float _BumpScale;
            fixed4 _Specular;
            float _Gloss;

            struct a2v{
                float4 vertex : POSITION;
                float3 normal : NORMAL;
                float4 tangent : TANGENT;
                float4 texcoord : TEXCOORD;
            }

            struct v2f{
                float3 pos : SV_POSITION;
                float3 lightDir : TEXCOORD0;
                float3 viewDir : TEXCOORD1;
                float4 uv : TEXCOORD2;
            }

            v2f vert(a2v v){
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv.xy = v.texcoord.xy * _MainTex_ST.xy + _MainTex_ST.zw;
                o.uv.zw = v.texcoord.zw * _BumpTex_ST.xy + _BumpTex_ST.zw;
                float3 binormal = cross(normalize(v.normal), normalize(v.tangent.xyz)) * v.tangent.w;
                float3x3 rotation = float3x3(v.tangent.xyz, binormal, v.normal);
                v.lightDir = mul(rotation, ObjectSpaceLightDir(v.vertex));
                v.viewDir = mul(rotation, ObjectSpaceViewDir(v.vertex));
                return o;
            }

            fixed4 frag(v2f i) : SV_Target{
                fixed3 albedo = tex2D(_MainTex, i.uv.xy);
                fixed4 packagedNormal = tex2D(_BumpTex, i.uv.zw);
                fixed3 tangentNormal = Unpackaged(packagedNormal);
                tangentNormal *= _BumpScale;
                fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo;
                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(i.lightDir, tangentNormal));
                float3 halfDir = normalize(v.lightDir + v.viewDir);
                fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(halfDir, tangentNormal)),_Gloss);
                return fixed4(ambient + diffuse + specular, 1.0);
            }

            ENDCG
        }
    }
    FallBack "Diffuse"
}
```

# 3. 环境映射

<center><img alt=图 3 src=../images/chapter5%20%E7%BA%B9%E7%90%86%E8%B4%B4%E5%9B%BE1763357610240.png ></center>

>使用立方体纹理将某点附近的环境光写入纹理，达到模拟金属反射的效果。

1. 使用脚本
```CSharp
    void GenerateCubemap()
    {
        GameObject go = new GameObject("CubemapCamera");
        go.AddComponent<Camera>();
        go.transform.position = renderFromPosition.position;
        go.GetComponent<Camera>().RenderToCubemap(cubemap);
        DestroyImmediate(go);
    }
```