# AutoML Leaderboard

| Best model   | name                                                       | model_type    | metric_type   |   metric_value |   train_time |
|:-------------|:-----------------------------------------------------------|:--------------|:--------------|---------------:|-------------:|
|              | [1_Default_LightGBM](1_Default_LightGBM/README.md)         | LightGBM      | logloss       |       0.930336 |        28.58 |
|              | [2_Default_Xgboost](2_Default_Xgboost/README.md)           | Xgboost       | logloss       |       0.945977 |        18.06 |
|              | [3_Default_CatBoost](3_Default_CatBoost/README.md)         | CatBoost      | logloss       |       0.923381 |        19.26 |
|              | [4_Default_RandomForest](4_Default_RandomForest/README.md) | Random Forest | logloss       |       1.00834  |        27.19 |
| **the best** | [Ensemble](Ensemble/README.md)                             | Ensemble      | logloss       |       0.907644 |         0.15 |

### AutoML Performance
![AutoML Performance](ldb_performance.png)

### AutoML Performance Boxplot
![AutoML Performance Boxplot](ldb_performance_boxplot.png)

### Features Importance
![features importance across models](features_heatmap.png)



### Spearman Correlation of Models
![models spearman correlation](correlation_heatmap.png)

