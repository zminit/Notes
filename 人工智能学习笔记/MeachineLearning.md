# 1. Fundamental concepts

## 1.1 Performance measure
### **错误率和精度**

$$
\begin{matrix}
    E(f;D) = \frac{1}{m}\sum\limits_{i=1}^m\mathbb{I}(f(x_i)\neq y_i) \\
    \mathbb{I}(f(x_i)\neq y_i) = 
    \begin{cases}
        1, f(x_i) \neq y_i \\ 0, f(x_i) = y_i    
    \end{cases}\\
    \text{acc}(f;D) = \frac{1}{m}\sum\limits_{i=1}^m\mathbb{I}(f(x_i) = y_i) = 1-E(f;D)
\end{matrix}
$$

$f:算法函数$

$D:数据分布$

### **Confusion Matrix**：混淆矩阵
||预测正例|预测反例|
|:---:|:---:|:---:|
|真实正例|TP(true positive)|FN(false negative)|
|真实反例|FP|TN|

### **precision**:查准率，精确率

$$P= \frac{TP}{TP+FP}$$

### **recall**:查全率，召回率
$$R=\frac{TP}{TP+FN}$$

>正例和反例都有对应的P和R

### **P-R曲线**
<center><img alt=图 1 src=../images/MeachineLearning1762071875908.png></center>
学习器得到的结果按照可能性排序，将每一个样本对应的可能性作为阈值进行分类，得到一个正例的P和R，将每个样本得到的P和R值作为横纵坐标就得到了一系列点，连接各点得到该学习器的P-R曲线。

**例如**：

>学习器output:[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
>
>真实分类:[0, 0, 1, 0, 0, 1, 1, 1, 0, 1]
>
>每个样本对应的P-R坐标(R, P):
>
>(1, 0.5), (0.55, 1), (0.625, 1), (0.8, 0.57), (0.8, 0.66), (0.8, 0.8), (0.75, 0.6), (0.4, 0.66), (0.2, 0.5), (0.2, 1)
>
>以上蓝色折线即样例的P-R曲线

**BEP**: P-R曲线中P=R时P或R的值

理想情况下判断学习器好坏看P-R曲线包裹情况，比如上例中绿色曲线完全包裹红色曲线，说明绿色学习器比红色优秀。

但实践中一般使用BEP衡量学习器好坏。

### **F1 Scroe**:F1分数
BEP过于简单，更常用的时F1分数

$$F1 = \frac{2\times P \times R}{P+R} = \frac{2\times TP}{样例总数 + TP - TN}$$

**$F_\beta$分数**

$$F_\beta = \frac{(1+\beta^2)\times P \times R}{(\beta^2\times P)+ R}$$

$$F1分数定义： \frac{1}{F1} = \frac{1}{P} + \frac{1}{R}$$
$$F_\beta = \frac{1}{1+\beta^2}(\frac{1}{P} + \frac{\beta^2}{R})$$

### 宏准确率、宏查全率、 宏F1分数
执行多折验证时需要进行宏观的性能分析

$$\large\begin{matrix}
    \text{macro-}P = \frac{1}{n}\sum\limits_{i=1}^n P_i\\
    \text{macro-}R = \frac{1}{n}\sum\limits_{i=1}^n R_i \\
\end{matrix}$$

$$\text{macro-}F1 = \frac{2\times \text{macro-}P \times \text{macro-}R}{\text{macro-}P + \text{macro-}R}$$

### **Balanced Accuracy**:平衡准确率

$$bacc = \frac{1}{n}\sum\limits_{i=1}^n R_i$$

$n：类别数$

$R_i：不同类别对应的召回率$

### ROC与AUC
<center><img alt=图 2 src=../images/MeachineLearning1762076813265.png width=400></center>
<center><img alt=图 3 src=../images/MeachineLearning1762077355732.png width=400></center>

**真正例率**：
$$TPR = \frac{TP}{TP+FN}$$

**假正例率**
$$FPR = \frac{FP}{TN + FP}$$

**ROC图：**
类似于P-R曲线，对学习器输出排序，以每个样本为阈值，得到一系列TPR和FPR, 连接成线

**AUC**: ROC图中曲线积分

**例如**：

>学习器output:[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
>
>真实分类:[0, 0, 1, 0, 0, 1, 1, 1, 0, 1]
>
>每个样本对应的ROC坐标(FPR, TPR):
>
>(1,1) (0.8,1) (0.6,1) (0.6,0.8) (0.4,0.8) (0.2,0.8) (0.2,0.6) (0.2,0.4) (0.2,0.2) (0.0,0.2)
>
>以上蓝色折线即样例的P-R曲线

绿色斜线为随机猜测理论ROC图

## 1.2 Validation methods

**5-splits cross validation**
```python
from sklearn.metrics import cross_val_score

bacc = cross_val_score(
    X,y,
    n_splits=5,
    random_state=42,
    score='balanced_accuracy'
)
```

# 2. Basic algorithm

## 2.1 SVC(支持向量机)
```python
import sklearn
import sklearn.SVM as SVM
from sklearn.model_selection import train_test_split
from sklearn.metrics import GridSearchCV, cross_val_predict



```

## 2.2 Random Forest

## 2.3 KNN