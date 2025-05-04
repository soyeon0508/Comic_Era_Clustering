import random
import os

INPUT_PATH = "image_label_list.txt"
OUTPUT_PATH = "image_label_list_partial.txt"
LABELED_RATIO = 0.1  # 전체 중 10%를 라벨링
SEED = 42

def split_labeled_unlabeled(filepath, labeled_ratio=0.1, seed=42):
    random.seed(seed)
    with open(filepath, 'r') as f:
        lines = f.readlines()

    random.shuffle(lines)
    num_labeled = int(len(lines) * labeled_ratio)

    labeled = lines[:num_labeled]
    unlabeled = lines[num_labeled:]

    labeled_data = [line.strip() for line in labeled]
    unlabeled_data = [line.strip().split(', ')[0] + ', -1' for line in unlabeled]

    return labeled_data + unlabeled_data

if __name__ == "__main__":
    result = split_labeled_unlabeled(INPUT_PATH, LABELED_RATIO, SEED)

    with open(OUTPUT_PATH, 'w') as f:
        for line in result:
            f.write(line + '\n')

    print(f"{OUTPUT_PATH} 생성 완료! 총 {len(result)}개 중 {int(len(result) * LABELED_RATIO)}개 라벨 유지됨.")

