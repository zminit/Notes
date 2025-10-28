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

Base Pass无论有多少光源，只执行一次