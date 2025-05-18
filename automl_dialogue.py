import os
import pandas as pd
import matplotlib.pyplot as plt
from supervised.automl import AutoML
from sklearn.metrics import accuracy_score, f1_score, adjusted_rand_score, normalized_mutual_info_score

# 경로 설정
RESULT_DIR = "/home/ubuntu/comic_translation/result_v1"
os.makedirs(RESULT_DIR, exist_ok=True)
csv_path = os.path.join(RESULT_DIR, "reduced_features_dialogue.csv")

# 데이터 로드
df = pd.read_csv(csv_path)
X = df.drop(columns=["label"])
y = df["label"]

# AutoML 설정
automl = AutoML(
    results_path=os.path.join(RESULT_DIR, "mljar_results"),
    mode="Explain",                     
    ml_task="multiclass_classification", # 분류 문제
    algorithms=['Random Forest', 'LightGBM', 'Xgboost', 'CatBoost'],  # 사용할 모델만 지정
    total_time_limit=600,                # 10분 제한
    explain_level=2,                     # 자세한 모델 설명 포함
    random_state=42                      # 결과 재현성 확보
)

# 모델 학습
print("MLJAR 모델 학습 중...")
automl.fit(X, y)
print("MLJAR 모델 학습 완료!")

# 모델 예측
predictions = automl.predict(X)

# 성능 평가
accuracy = accuracy_score(y, predictions)
f1 = f1_score(y, predictions, average='weighted')
ari = adjusted_rand_score(y, predictions)
nmi = normalized_mutual_info_score(y, predictions)

# 성능 출력
print(f"Accuracy: {accuracy:.4f}")
print(f"F1 Score: {f1:.4f}")
print(f"ARI: {ari:.4f}")
print(f"NMI: {nmi:.4f}")

# 성능 저장
with open(os.path.join(RESULT_DIR, "mljar_performance.txt"), "w") as f:
    f.write(f"Accuracy: {accuracy:.4f}\n")
    f.write(f"F1 Score: {f1:.4f}\n")
    f.write(f"ARI: {ari:.4f}\n")
    f.write(f"NMI: {nmi:.4f}\n")
print("성능 저장 완료!")

