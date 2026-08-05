# 尽量用const,enum,inline替代#define

```cpp
#define PI 3.14
const double PI = 3.14
```

- #define定义的**记号**不会被编译器看见，出错时报告给出的是数字而不是符号，增加debug工作量。
- #define定义的宏会被预处理器盲目的替换，会导致一个较小的码被复制多份。（这部分是怎么回事，浮点数不是直接被放到源码中的吗，应该不占内存吧）
- 