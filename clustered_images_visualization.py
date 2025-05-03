import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

SAVE_DIR = "/home/ubuntu/comic_translation/result_v3"

embeddings = np.load(os.path.join(SAVE_DIR, "embeddings.npy"))
labels_true = np.load(os.path.join(SAVE_DIR, "labels_true.npy"))
labels_pred = np.load(os.path.join(SAVE_DIR, "labels_pred.npy"))

def visualize(data, labels, title, filename, label_name="Label"):
    reduced = PCA(n_components=2).fit_transform(data)
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(reduced[:, 0], reduced[:, 1], c=labels, cmap="tab10", alpha=0.6)
    plt.colorbar(scatter, ticks=np.unique(labels), label=label_name)
    plt.title(title)
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(SAVE_DIR, filename))
    plt.close()

visualize(embeddings, labels_pred, "KMeans Clustering (Image, k=3)", "image_cluster_plot.png", label_name="Cluster")
visualize(embeddings, labels_true, "True Label Distribution (Image)", "image_true_label_plot.png", label_name="True Label")
print("✅ 시각화 완료 및 저장!")

