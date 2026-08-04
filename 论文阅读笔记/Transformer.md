# 1. Model Architecture

<center><img alt=图 0 src=../images/Transformer1758955209172.png></center>

## 1.1 Recurrent Nerual Network

<center><img alt=图 13 src=../images/Transformer1759995321260.png></center>

>单向RNN

<center><img alt=图 12 src=../images/Transformer1759995292212.png width=400></center>

>双向RNN

<center><img alt=图 17 src=../images/Transformer1759996952968.png></center>

双向RNN相当于将输入序列正向和反向同时进行一次计算，并将正向计算得到的$\overrightarrow{h_t}$和反向得到的$\overleftarrow{h_t}$拼接在一起得到的两倍$h_t$大小的序列作为输出层$O$的输入。

## 1.2 LSTMs
如下为LSTM单元结构：
<center><img alt=图 7 src=../images/Transformer1759210755292.png></center>

双向LSTM与双向RNN类似，将输入序列正向和反向计算一次，最后将得到的$h_t$拼接在一起。
## 1.3 Attention mechanism

### 1.3.1 Encoder-Decoder
在《NEURAL MACHINE TRANSLATION BY JOINTLY LEARNING TO ALIGN AND TRANSLATE》中

之前版本的Encoder-Encoder架构

<center><img alt=图 25 src=../images/Transformer1760083283645.png></center>

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

由此可知，注意力机制提出之前，上下文信息c是固定不变的，Decoder的输入为c和上一次生成的y

### 1.3.2 Proposted Architecture
**论文提出不断改变c的值实现对长序列生成效果的提升**

$$
\large
\begin{matrix}
    p(y_i \mid y_1, \dots,y_{i-1}, \bold{x}) = g(y_{i-1}, s_i, c_i) \\
    s_i = f(s_{i-1}, y_{i-1}, c_i) \\
    c_i = \sum\limits_{j=1}^{T_x}\alpha_{ij}h_j \\
    \alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k=1}^{T_x}\exp(e_{ik})} \\
    e_{ij} = a(s_{i-1}, h_j)
\end{matrix}
$$

>下图为论文中新模型的总结构概略图

<center><img alt=图 30 src=../images/Transformer1760084165127.png></center>

>下图为论文中使用的Encoder中双向RNN中的一个方向的网络结构
<center><img alt=图 21 src=../images/Transformer1760074820541.png></center>

$x_i$：一个token。

$E_{x_i}$：词嵌入。

$z_i$：更新门输出，用于确定哪些内容需要记忆，$(1-z_i)$则指示哪些内容需要遗忘。

$r_i$：复位门输出。

$\bar{E} \in \mathbf{R}^{m\times K_x}$

$W,W_z, W_r \in \mathbf{R}^{n\times m}$

$U,U_z, U_r \in \mathbf{R}^{n\times n}$

$C,C_z,C_r \in \mathbf{R}^{n\times 2n}$


>下图为论文中使用的Decoder中RNN的一个单元

<center><img alt=图 22 src=../images/Transformer1760082915136.png></center>

$W,W_z, W_r \in \mathbf{R}^{n\times m}$

$U,U_z, U_r \in \mathbf{R}^{n\times n}$

$C,C_z,C_r \in \mathbf{R}^{n\times 2n}$

初始状态$s_0 = \tanh(W_s \overleftarrow{h_1}), W_s \in \mathbf{R}^{n\times n}$

>下图为论文中动态计算$c_i$的模型结构

<center><img alt=图 28 src=../images/Transformer1760084139489.png width=400></center>

$$
\begin{matrix}
    c_i = \sum\limits_{j=1}^{T_x} \alpha_{ij}h_j \\
    \large
    \alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k=1}^{T_x}\exp(e_{ik})} 
    \normalsize\\
    e_{ij} = v_a^T \tanh(W_a s_{i-1} + U_a h_j)
\end{matrix}
$$

$v_a \in \mathbf{R}^{n^\prime}, W_a \in \mathbf{R}^{n^\prime \times n}, U_a \in \mathbf{R}^{n^\prime \times 2n}$

$W_o \in \mathbf{R}^{K_y \times l}, U_o \in \mathbf{R}^{2l \times n}, V_o \in \mathbf{R}^{2l\times m}, C_o \in \mathbf{R}^{2l\times 2n}$


### 1.3.3 attention

该论文提出的注意力机制主要用于序列生成任务中的上下文信息$c_i$的生成，大概机制就是利用$U_a, W_a, v_a$三个矩阵（其中$v_a$是一个一维向量），使用Decoder的上一个隐藏状态$s_{i-1}$和Encoder的输出$\bold{h}$计算出向量组$\bold{h}$中的每一个$h_j$对应的注意力分数$e_{ij}$，并将其作为权重与各自对应的$h_j$相乘相加得到第$i$步的上下文信息。

## 1.4 Nerual Encoder-Decoder
如下为《A DEEP REINFORCED MODEL FOR ABSTRACTIVE
SUMMARIZATION》一文中处理语言问题的神经编码-解码器结构图：
<center><img alt=图 1 src=../images/Transformer1759067191962.png></center>

<center><img alt=图 6 src=../images/Transformer1759067839808.png></center>






# 2. Transformer架构