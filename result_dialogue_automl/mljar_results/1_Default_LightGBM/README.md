# Summary of 1_Default_LightGBM

[<< Go back](../README.md)


## LightGBM
- **n_jobs**: -1
- **objective**: multiclass
- **num_leaves**: 63
- **learning_rate**: 0.05
- **feature_fraction**: 0.9
- **bagging_fraction**: 0.9
- **min_data_in_leaf**: 10
- **metric**: multi_logloss
- **custom_eval_metric_name**: None
- **num_class**: 3
- **explain_level**: 2

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.75
 - **shuffle**: True
 - **stratify**: True

## Optimized metric
logloss

## Training time

28.0 seconds

### Metric details
|           |      VL_01 |      VL_02 |      VL_03 |   accuracy |   macro avg |   weighted avg |   logloss |
|:----------|-----------:|-----------:|-----------:|-----------:|------------:|---------------:|----------:|
| precision |   0.471429 |   0.542056 |   0.595174 |    0.55726 |    0.53622  |       0.547602 |  0.930336 |
| recall    |   0.157895 |   0.745501 |   0.584211 |    0.55726 |    0.495869 |       0.55726  |  0.930336 |
| f1-score  |   0.236559 |   0.627706 |   0.589641 |    0.55726 |    0.484635 |       0.529327 |  0.930336 |
| support   | 209        | 389        | 380        |    0.55726 |  978        |     978        |  0.930336 |


## Confusion matrix
|                  |   Predicted as VL_01 |   Predicted as VL_02 |   Predicted as VL_03 |
|:-----------------|---------------------:|---------------------:|---------------------:|
| Labeled as VL_01 |                   33 |                  109 |                   67 |
| Labeled as VL_02 |                   15 |                  290 |                   84 |
| Labeled as VL_03 |                   22 |                  136 |                  222 |

## Learning curves
![Learning curves](learning_curves.png)

## Permutation-based Importance
![Permutation-based Importance](permutation_importance.png)
## Confusion Matrix

![Confusion Matrix](confusion_matrix.png)


## Normalized Confusion Matrix

![Normalized Confusion Matrix](confusion_matrix_normalized.png)


## ROC Curve

![ROC Curve](roc_curve.png)


## Precision Recall Curve

![Precision Recall Curve](precision_recall_curve.png)



[<< Go back](../README.md)
