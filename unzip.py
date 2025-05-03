import os
import zipfile

def unzip_all_zips_in_directory(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".zip"):
                zip_path = os.path.join(subdir, file)
                output_folder = os.path.join(subdir, os.path.splitext(file)[0])
                os.makedirs(output_folder, exist_ok=True)

                print(f"📦 압축 해제 중: {zip_path}")
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(output_folder)
                    print(f"✅ 완료: {output_folder}\n")
                except zipfile.BadZipFile:
                    print(f"❌ 오류: {zip_path}는 손상된 zip 파일입니다.\n")

# 사용 예시
root_data_path = "/home/ubuntu/comic_translation/Validation"
unzip_all_zips_in_directory(root_data_path)

