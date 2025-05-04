import os

# 파일 이름과 라벨 매핑
file_label_map = {
    "VL_01_dialogues.txt": "VL_01",
    "VL_02_dialogues.txt": "VL_02",
    "VL_03_dialogues.txt": "VL_03"
}

output_file = "labeled_dialogues.txt"

with open(output_file, 'w', encoding='utf-8') as out_f:
    for filename, label in file_label_map.items():
        if not os.path.exists(filename):
            print(f"파일 없음: {filename}")
            continue

        with open(filename, 'r', encoding='utf-8') as in_f:
            for line in in_f:
                line = line.strip()
                if line:
                    out_f.write(f"{label}\t{line}\n")

print(f"병합 및 라벨링 완료 → {output_file}")

