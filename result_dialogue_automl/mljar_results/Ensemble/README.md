# Summary of Ensemble

[<< Go back](../README.md)


## Ensemble structure
| Model                             |   Weight |
|:----------------------------------|---------:|
| 18_CatBoost                       |        1 |
| 20_Xgboost                        |        1 |
| 3_Default_CatBoost                |        1 |
| 3_Default_CatBoost_GoldenFeatures |        1 |
| 5_Xgboost                         |        1 |

### Metric details
|           |      VL_01 |       VL_02 |       VL_03 |   accuracy |   macro avg |   weighted avg |   logloss |
|:----------|-----------:|------------:|------------:|-----------:|------------:|---------------:|----------:|
| precision |   0.584615 |    0.564275 |    0.584699 |   0.574572 |    0.577863 |       0.576551 |  0.904425 |
| recall    |   0.227545 |    0.702442 |    0.634387 |   0.574572 |    0.521458 |       0.574572 |  0.904425 |
| f1-score  |   0.327586 |    0.625823 |    0.608531 |   0.574572 |    0.520647 |       0.555402 |  0.904425 |
| support   | 835        | 1556        | 1518        |   0.574572 | 3909        |    3909        |  0.904425 |


## Confusion matrix
|                  |   Predicted as VL_01 |   Predicted as VL_02 |   Predicted as VL_03 |
|:-----------------|---------------------:|---------------------:|---------------------:|
| Labeled as VL_01 |                  190 |                  353 |                  292 |
| Labeled as VL_02 |                   71 |                 1093 |                  392 |
| Labeled as VL_03 |                   64 |                  491 |                  963 |

## Learning curves
![Learning curves](learning_curves.png)
## Confusion Matrix

![Confusion Matrix](confusion_matrix.png)


## Normalized Confusion Matrix

![Normalized Confusion Matrix](confusion_matrix_normalized.png)


## ROC Curve

![ROC Curve](roc_curve.png)


## Precision Recall Curve

![Precision Recall Curve](precision_recall_curve.png)



[<< Go back](../README.md)
