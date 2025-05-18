import os
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

# 경로 설정
RESULT_DIR = "/home/ubuntu/comic_translation/result_v1"
os.makedirs(RESULT_DIR, exist_ok=True)

# 데이터 로드
embeddings = np.load(os.path.join(RESULT_DIR, "embeddings.npy"))
labels = np.load(os.path.join(RESULT_DIR, "labels.npy"))

print(f"임베딩 크기: {embeddings.shape}")
print(f"레이블 개수: {len(labels)}")

# 차원 축소 (PCA)
print("차원 축소 중 (PCA)...")
pca = PCA(n_components=128, random_state=42)
reduced_embeddings = pca.fit_transform(embeddings)
print(f"PCA 변환 후 크기: {reduced_embeddings.shape}")

# DataFrame으로 변환
df = pd.DataFrame(reduced_embeddings, columns=[f"feat_{i}" for i in range(128)])
df['label'] = labels

# 데이터 저장
csv_path = os.path.join(RESULT_DIR, "reduced_features.csv")
df.to_csv(csv_path, index=False)
print(f"데이터 저장 완료: {csv_path}")
