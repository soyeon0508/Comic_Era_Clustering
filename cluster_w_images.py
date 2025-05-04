import os
import torch
import numpy as np
from PIL import Image
from tqdm import tqdm
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from torchvision import models, transforms

SAVE_DIR = "/home/ubuntu/comic_translation/result_v2"
os.makedirs(SAVE_DIR, exist_ok=True)

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.fc = torch.nn.Identity()
model = model.to(device)
model.eval()

def load_image_label_list(file_path):
    image_paths, labels = [], []
    with open(file_path, 'r') as f:
        for line in f:
            path, label = line.strip().split()
            image_paths.append(path)
            labels.append(label)
    return image_paths, labels

def embed_images(image_paths):
    embeddings, valid_paths = [], []
    with torch.no_grad():
        for path in tqdm(image_paths, desc="이미지 임베딩 중", ncols=80):
            try:
                img = Image.open(path).convert("RGB")
                img = preprocess(img).unsqueeze(0).to(device)
                feat = model(img).squeeze().cpu().numpy()
                embeddings.append(feat)
                valid_paths.append(path)
            except:
                continue
    return np.array(embeddings), valid_paths

def save_cluster_samples(image_paths, embeddings, labels, kmeans, k=3):
    for i in range(k):
        cluster_dir = os.path.join(SAVE_DIR, f"cluster_{i}_samples")
        os.makedirs(cluster_dir, exist_ok=True)
        indices = [j for j, lbl in enumerate(labels) if lbl == i]
        cluster_embs = embeddings[indices]
        center = kmeans.cluster_centers_[i]
        dists = np.linalg.norm(cluster_embs - center, axis=1)
        top_k = np.argsort(dists)[:10]
        for rank, idx in enumerate(top_k):
            src = image_paths[indices[idx]]
            dst = os.path.join(cluster_dir, f"rank{rank+1}_{os.path.basename(src)}")
            try:
                Image.open(src).save(dst)
            except:
                continue

if __name__ == "__main__":
    image_paths, label_strs = load_image_label_list("image_label_list.txt")
    label_map = {s: i for i, s in enumerate(sorted(set(label_strs)))}
    true_labels = [label_map[lbl] for lbl in label_strs]

    embeddings, valid_paths = embed_images(image_paths)
    true_labels = [label_map[label_strs[i]] for i in range(len(image_paths)) if image_paths[i] in valid_paths]

    k = 3
    kmeans = KMeans(n_clusters=k, random_state=42)
    pred_labels = kmeans.fit_predict(embeddings)

    ari = adjusted_rand_score(true_labels, pred_labels)
    nmi = normalized_mutual_info_score(true_labels, pred_labels)
    with open(os.path.join(SAVE_DIR, "cluster_scores.txt"), 'w') as f:
        f.write(f"ARI: {ari:.4f}\nNMI: {nmi:.4f}\n")

    save_cluster_samples(valid_paths, embeddings, pred_labels, kmeans, k=k)

    np.save(os.path.join(SAVE_DIR, "embeddings.npy"), embeddings)
    np.save(os.path.join(SAVE_DIR, "labels_true.npy"), np.array(true_labels))
    np.save(os.path.join(SAVE_DIR, "labels_pred.npy"), np.array(pred_labels))

    print("클러스터링 완료 및 결과 저장!")

