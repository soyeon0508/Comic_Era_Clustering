import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.semi_supervised import LabelSpreading
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
import shutil

SAVE_DIR = "/home/ubuntu/comic_translation/result_v3"
PARTIAL_LABEL_PATH = "image_label_list_partial.txt"

# 1. Load embeddings
embeddings = np.load(os.path.join(SAVE_DIR, "embeddings.npy"))

# 2. Load partial labels
label_map = {"VS_01": 0, "VS_02": 1, "VS_03": 2}
paths = []
labels_raw = []

with open(PARTIAL_LABEL_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip().replace(',', ' ')
        parts = line.split()

        if len(parts) >= 2:
            path = parts[0]
            label_str = parts[-1]
            if label_str in label_map:
                labels_raw.append(label_map[label_str])
                paths.append(path)
            elif label_str == "-1":
                labels_raw.append(-1)
                paths.append(path)
            else:
                print("알 수 없는 라벨:", label_str)
        else:
            print("잘못된 줄:", line)

labels = np.array(labels_raw)
print(f"Labeled: {(labels != -1).sum()}, Unlabeled: {(labels == -1).sum()}")

# 3. Run Label Spreading
model = LabelSpreading(kernel='rbf', alpha=0.8, max_iter=1000)
model.fit(embeddings, labels)
pred = model.transduction_
np.save(os.path.join(SAVE_DIR, "labels_pred_spread.npy"), pred)

# 4. Evaluate
if os.path.exists(os.path.join(SAVE_DIR, "labels_true.npy")):
    labels_true = np.load(os.path.join(SAVE_DIR, "labels_true.npy"))
    ari = adjusted_rand_score(labels_true, pred)
    nmi = normalized_mutual_info_score(labels_true, pred)
    with open(os.path.join(SAVE_DIR, "semi_spread_scores.txt"), 'w') as f:
        f.write(f"ARI: {ari:.4f}\n")
        f.write(f"NMI: {nmi:.4f}\n")
    print(f"평가 완료 (ARI: {ari:.4f}, NMI: {nmi:.4f})")

# 5. 시각화 저장
pca = PCA(n_components=2)
reduced = pca.fit_transform(embeddings)

plt.figure(figsize=(10, 8))
scatter = plt.scatter(reduced[:, 0], reduced[:, 1], c=pred, cmap='tab10', alpha=0.6)
plt.title("Label Spreading Result (k=3)")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.colorbar(scatter, ticks=[0, 1, 2], label="Predicted Label")
plt.grid(True)
plt.savefig(os.path.join(SAVE_DIR, "semi_spread_plot.png"))
plt.close()

# 6. Cluster별 대표 이미지 저장
for c in np.unique(pred):
    indices = np.where(pred == c)[0]
    cluster_dir = os.path.join(SAVE_DIR, f"cluster_{c}_samples")
    os.makedirs(cluster_dir, exist_ok=True)

    # 거리 기반 정렬 (중심에 가까운 것 순으로)
    center = embeddings[indices].mean(axis=0)
    dists = np.linalg.norm(embeddings[indices] - center, axis=1)
    sorted_idx = indices[np.argsort(dists)[:10]]

    for rank, idx in enumerate(sorted_idx):
        img_path = paths[idx]
        if not os.path.exists(img_path):
            continue
        ext = os.path.splitext(os.path.basename(img_path))[1]
        dst = os.path.join(cluster_dir, f"rank{rank+1}_{os.path.basename(img_path)}")
        shutil.copy(img_path, dst)

