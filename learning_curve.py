import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.semi_supervised import LabelSpreading
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.decomposition import PCA

SAVE_DIR = "/home/ubuntu/comic_translation/result_v5"
embedding_path = os.path.join(SAVE_DIR, "embeddings.npy")
label_path = os.path.join(SAVE_DIR, "labels_true.npy")

embeddings = np.load(embedding_path)
labels_true = np.load(label_path)
n_samples = len(labels_true)

ratios = [0.01, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0]
ari_scores = []
nmi_scores = []

score_log_path = os.path.join(SAVE_DIR, "learning_curve_scores.txt")
with open(score_log_path, 'w') as f_log:
    f_log.write("Ratio\tARI\tNMI\n")

    for ratio in ratios:
        n_labeled = int(n_samples * ratio)
        indices = np.random.permutation(n_samples)
        labeled_indices = indices[:n_labeled]

        labels = np.full(n_samples, -1)
        labels[labeled_indices] = labels_true[labeled_indices]

        model = LabelSpreading(kernel='rbf', alpha=0.8, max_iter=1000)
        model.fit(embeddings, labels)
        pred = model.transduction_

        ari = adjusted_rand_score(labels_true, pred)
        nmi = normalized_mutual_info_score(labels_true, pred)
        ari_scores.append(ari)
        nmi_scores.append(nmi)
        print(f"✅ Ratio {ratio:.2f} → ARI: {ari:.4f}, NMI: {nmi:.4f}")
        f_log.write(f"{ratio:.2f}\t{ari:.4f}\t{nmi:.4f}\n")

        # 시각화 저장
        reduced = PCA(n_components=2).fit_transform(embeddings)
        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(reduced[:, 0], reduced[:, 1], c=pred, cmap='tab10', alpha=0.6)
        plt.title(f"Label Spreading Clustering (Ratio={int(ratio*100)}%)")
        plt.xlabel("PCA 1")
        plt.ylabel("PCA 2")
        plt.colorbar(scatter, ticks=[0, 1, 2], label="Predicted Label")
        plt.grid(True)
        plot_path = os.path.join(SAVE_DIR, f"plot_ratio_{int(ratio*100)}.png")
        plt.savefig(plot_path)
        plt.close()

# 최종 학습 곡선 저장
plt.figure(figsize=(10, 6))
plt.plot(ratios, ari_scores, marker='o', label="ARI")
plt.plot(ratios, nmi_scores, marker='s', label="NMI")
plt.xlabel("Labeled Data Ratio")
plt.ylabel("Score")
plt.title("Learning Curve: Label Spreading")
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(SAVE_DIR, "learning_curve_plot.png"))
plt.close()

