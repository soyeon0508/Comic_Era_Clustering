import os
import pandas as pd
import matplotlib.pyplot as plt
from supervised.automl import AutoML
from sklearn.metrics import accuracy_score, f1_score, adjusted_rand_score, normalized_mutual_info_score

# 경로 설정
RESULT_DIR = "/home/ubuntu/comic_translation/result_v1"
os.makedirs(RESULT_DIR, exist_ok=True)
csv_path = os.path.join(RESULT_DIR, "reduced_features.csv")

# 데이터 로드
df = pd.read_csv(csv_path)
X = df.drop(columns=["label"])
y = df["label"]

# AutoML 설정
automl = AutoML(
    results_path=os.path.join(RESULT_DIR, "mljar_results"),
    mode="Perform",                     
    ml_task="multiclass_classification", # 분류 문제
    algorithms=['Random Forest', 'LightGBM', 'Xgboost', 'CatBoost'],  # 사용할 모델만 지정
    total_time_limit=1800,               # 30분 제한
    explain_level=2,                     # 자세한 모델 설명 포함
    random_state=42                      # 결과 재현성 확보
)

# 모델 학습
print("MLJAR 모델 학습 중...")
automl.fit(X, y)
print("MLJAR 모델 학습 완료!")

# 모든 모델 리스트 확인
leaderboard = automl.get_leaderboard()
model_performance = []

# 각 모델별로 예측 수행 및 성능 평가
for idx, row in leaderboard.iterrows():
    model_name = row['model']
    model_path = row['path']
    try:
        # 모델 로드
        model = AutoML(results_path=model_path)
        predictions = model.predict(X)

        # 성능 평가
        accuracy = accuracy_score(y, predictions)
        f1 = f1_score(y, predictions, average='weighted')
        ari = adjusted_rand_score(y, predictions)
        nmi = normalized_mutual_info_score(y, predictions)

        # 결과 저장
        model_performance.append((model_name, accuracy, f1, ari, nmi))
        print(f"Model: {model_name} -> Accuracy: {accuracy:.4f}, F1: {f1:.4f}, ARI: {ari:.4f}, NMI: {nmi:.4f}")
    except Exception as e:
        print(f"Error with model {model_name}: {e}")

# 성능 데이터프레임 생성
df_performance = pd.DataFrame(model_performance, columns=["Model", "Accuracy", "F1", "ARI", "NMI"])

# 결과 출력 및 저장
print("\nModel Performance (Accuracy, F1, ARI, NMI):")
print(df_performance)

performance_path = os.path.join(RESULT_DIR, "all_models_performance.csv")
df_performance.to_csv(performance_path, index=False)
print(f"\n모든 모델 성능 저장 완료: {performance_path}")
