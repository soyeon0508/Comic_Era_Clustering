import os
import json

def extract_dialogues_by_subfolders(root_label_paths):
    for base_path in root_label_paths:
        if not os.path.exists(base_path):
            print(f"❌ 경로 없음: {base_path}")
            continue

        for subfolder in os.listdir(base_path):
            folder_path = os.path.join(base_path, subfolder)
            if not os.path.isdir(folder_path):
                continue

            all_dialogues = []

            for fname in os.listdir(folder_path):
                if not fname.endswith('.json'):
                    continue
                fpath = os.path.join(folder_path, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        contexts = data.get("label", {}).get("directing", {}).get("context", [])
                        for ctx in contexts:
                            dialogue = ctx.get("dialogue", "").strip()
                            if dialogue:
                                all_dialogues.append(dialogue)
                except Exception as e:
                    print(f"❌ 오류: {fname} → {e}")

            all_dialogues = sorted(set(all_dialogues))
            output_path = f"{subfolder}_dialogues.txt"

            with open(output_path, 'w', encoding='utf-8') as out:
                for line in all_dialogues:
                    out.write(line + '\n')

            print(f"✅ {subfolder}: {len(all_dialogues)}개 대사 추출 완료 → {output_path}")


if __name__ == "__main__":
    extract_dialogues_by_subfolders([
        "/home/ubuntu/comic_translation/Validation/02.label"
    ])

