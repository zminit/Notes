# 1. Shader创建
>`Assert`->`create`->`shader`
- Standard Surface Shader:包含标准光照模型，基于物理的渲染shader
- Unlit Shader:不包含光照的基本顶点/片元着色器
- Image Effect Shader:屏幕后处理shader
- Compute Shader:用于与渲染无关的计算

# 2. ShaderLab
>一种编写Unity Shader的说明性语言

```shaderlab
Shader "name1/name2"{
    Properties{//属性}
    SubShader{
        //表面着色器（Surface Shader）
        //顶点/片元着色器（Vertex/Fragment Shader）
        //固定函数着色器（Fixed Function Shader）
    }
    SubShader{}
    Fallback "..."
}
```
### 2.1 Properties
- 基础结构：
```shaderlab
Properties{
    Name ("name", PropertyType)=DefaultValue
    ...
}
```
<center><img alt=图 0 src=../images/chapter2%20UnityShader%E5%9F%BA%E7%A1%801747207516798.png></center>

### 2.2 SubShader
>Unity会扫描所有的`SubShader`，并采用第一个能在当前平台运行的shader，否则就使用`Fallback`指定的shader

```shaderlab
SubShader{
    [Tags]//可选
    Tags {"TagName"="Value" "TagName2"="Value2"}

    [RenderSetup]//可选

    Pass{
        [Tags]

        [RenderSetup]

    }
}
```
- **SubShader中的Tags**
<center><img alt=图 1 src=../images/chapter2%20UnityShader%E5%9F%BA%E7%A1%801747208204757.png></center>

### 2.3 Pass

```shaderlab
Pass{
    [Name]
    Name "MyPass"

    [Tags]
    [RenderSetup]
}

UsePass "ShaderName/MYPASS"
```
>UsePass命令会将所有的Pass的名字大写

- **Pass中的Tags**
<center><img alt=图 2 src=../images/chapter2%20UnityShader%E5%9F%BA%E7%A1%801747209197109.png></center>

### 2.4 Fallback

```shaderlab
Fallback "Name"
Fallback off
```

# 3. Shader们
### 3.1 SurfaceShader
>Unity对一些顶点/片元着色器包装为表面着色器
```shaderlab
SubShader {
    Tags{"RenderType" = "Opaque"}
    CGPROGRAM
    #pragma surface surf Lambert
    struct Input{
        float4 color : COLOR;
    };
    void surf (Input IN, inout SurfaceOutput o){
        o.Albedo = 1;
    }
    ENDCG
}
```

### 3.2 Vertex/Fragment Shader
```shaderlab
SubShader{
    Pass {
        CGPROGRAM
        #pragma vertex vert
        #pargma fragment frag

        float4 vert{float4 v : POSITION} : SV_POSITION {
            return mul (UNITY_MAXTRIX_MVP, v);
        } 
        ENDCG
    }
}
```
