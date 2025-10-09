# 1. Model Architecture

<center><img alt=图 0 src=../images/Transformer1758955209172.png></center>

## 1.1 Relevant paper

### 1.1.1 Recurrent Nerual Network

<center><img alt=图 11 src=../images/Transformer1759991980575.png></center>

### 1.1.1 Nerual Encoder-Decoder
如下为《A DEEP REINFORCED MODEL FOR ABSTRACTIVE
SUMMARIZATION》一文中处理语言问题的神经编码-解码器结构图：
<center><img alt=图 1 src=../images/Transformer1759067191962.png></center>

<center><img alt=图 6 src=../images/Transformer1759067839808.png></center>

### 1.1.2 LSTMs
如下为LSTM单元结构：
<center><img alt=图 7 src=../images/Transformer1759210755292.png></center>



### 1.1.3 Attention mechanism
在《NEURAL MACHINE TRANSLATION BY JOINTLY LEARNING TO ALIGN AND TRANSLATE》中提出
$$
\large
\begin{matrix}
    h_t = f(x_t, h_{t-1}) \\
    c = q(\{h_1, \dots, h_{T_x}\}) \\
    p(\bold{y}) = \prod\limits_{t=1}^T p(y_t | \{y_1, \dots, y_{t-1}\}, c)\\
    p(y_t | \{y_1, \dots, y_{t-1}\}, c) = g(y_{t-1}, s_t, c)
\end{matrix}
$$
$x_t$: 输入`tokens`转换成的定长数组，一般为词嵌入结果。

$h_t$: 隐藏状态(hidden state), 比如LSTM中的`Previous Outpus`。

$c$: 上下文序列(**context vector**)。

$f,q$: 非线性函数，比如LSTM就是一种非线性函数(nonlinear function)。

$p(\bold{y})$: 输出序列$\bold{y}$的概率。

$s_t$: RNN中的隐藏状态。


