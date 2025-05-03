import os
import matplotlib.pyplot as plt
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from collections import defaultdict

# 결과 저장 폴더
RESULT_DIR = "/home/ubuntu/comic_translation/result_v2"
os.makedirs(RESULT_DIR, exist_ok=True)

# 데이터 로드
labels = []
dialogues = []
with open("labeled_dialogues.txt", 'r', encoding='utf-8') as f:
    for line in f:
        label, text = line.strip().split('\t')
        labels.append(label)
        dialogues.append(text)

# 라벨 인코딩
label_encoder = LabelEncoder()
true_labels = label_encoder.fit_transform(labels)

# SBERT 임베딩
print("🔄 SBERT 임베딩 중...")
model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")
embeddings = model.encode(dialogues)
print("✅ 임베딩 완료!")

# KMeans 클러스터링
kmeans = KMeans(n_clusters=3, random_state=42)
pred_clusters = kmeans.fit_predict(embeddings)

# 클러스터링 평가
ari = adjusted_rand_score(true_labels, pred_clusters)
nmi = normalized_mutual_info_score(true_labels, pred_clusters)
with open(os.path.join(RESULT_DIR, "cluster_scores.txt"), 'w', encoding='utf-8') as f:
    f.write(f"Adjusted Rand Index (ARI): {ari:.4f}\n")
    f.write(f"Normalized Mutual Information (NMI): {nmi:.4f}\n")
print("📄 클러스터링 평가 저장 완료")

# PCA 축소
reduced = PCA(n_components=2).fit_transform(embeddings)

# 📊 클러스터링 결과 시각화
plt.figure(figsize=(10, 8))
scatter = plt.scatter(reduced[:, 0], reduced[:, 1], c=pred_clusters, cmap='tab10', vmin=0, vmax=2, alpha=0.6)
plt.colorbar(scatter, ticks=[0, 1, 2], label="Cluster ID")
plt.title("SBERT + KMeans Clustering (k=3)")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.grid(True)
plt.savefig(os.path.join(RESULT_DIR, "cluster_plot_k3.png"))
plt.close()
print("✅ 클러스터링 시각화 저장 완료")

# 📊 실제 정답 라벨 시각화
plt.figure(figsize=(10, 8))
scatter2 = plt.scatter(reduced[:, 0], reduced[:, 1], c=true_labels, cmap='Set2', vmin=0, vmax=2, alpha=0.6)
plt.colorbar(scatter2, ticks=[0, 1, 2], label="True Label (VL_01/02/03)")
plt.title("True Labels Distribution")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.grid(True)
plt.savefig(os.path.join(RESULT_DIR, "true_label_plot.png"))
plt.close()
print("✅ 정답 라벨 시각화 저장 완료")

# 📂 클러스터별 문장 30개씩 저장
clusters = defaultdict(list)
for text, cluster_id in zip(dialogues, pred_clusters):
    clusters[cluster_id].append(text)

for cid, lines in clusters.items():
    path = os.path.join(RESULT_DIR, f"cluster_{cid}_sample30.txt")
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines[:30]:
            f.write(line + '\n')
print("✅ 클러스터별 대표 문장 저장 완료")

