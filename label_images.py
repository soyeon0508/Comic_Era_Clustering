import os

# VS 폴더들이 있는 상위 디렉토리 경로
base_dir = "/home/ubuntu/comic_translation/Validation/01.source"
output_file = "image_label_list.txt"

with open(output_file, 'w', encoding='utf-8') as f_out:
    for label_folder in ["VS_01", "VS_02", "VS_03"]:
        folder_path = os.path.join(base_dir, label_folder)
        if not os.path.isdir(folder_path):
            print(f"❌ 폴더 없음: {folder_path}")
            continue

        for fname in os.listdir(folder_path):
            if fname.lower().endswith((".jpg", ".jpeg", ".png")):
                full_path = os.path.join(folder_path, fname)
                f_out.write(f"{full_path}\t{label_folder}\n")

print(f"✅ image_label_list.txt 생성 완료!")

