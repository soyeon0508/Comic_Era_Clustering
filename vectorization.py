import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

RESULT_DIR = "/home/ubuntu/comic_translation/result_v1"
os.makedirs(RESULT_DIR, exist_ok=True)

labels = []
dialogues = []

# 대사 파일 로드
with open("labeled_dialogues.txt", 'r', encoding='utf-8') as f:
    for line in f:
        label, text = line.strip().split('\t')
        labels.append(label)
        dialogues.append(text)

# SBERT 임베딩 생성
print("SBERT 임베딩 중...")
model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")
embeddings = model.encode(dialogues)
print("임베딩 완료!")

# 임베딩 및 라벨 저장
np.save(os.path.join(RESULT_DIR, "embeddings.npy"), embeddings)
np.save(os.path.join(RESULT_DIR, "labels.npy"), np.array(labels))
print("임베딩 데이터 저장 완료!")

