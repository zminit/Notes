# 1. Fundamental concepts

## 1.1 Evaluation indexs
**Accuracy**: 结果准确率

**Balanced Accuracy**:平衡准确率

**F1 Scroe**:F1分数

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