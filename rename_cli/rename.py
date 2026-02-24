import os

print("파일 이름 정리 도구")

path = input("정리할 폴더 경로 입력: ")
dry_run = input("dry-run 모드? (y/n): ").lower() == "y"

files = os.listdir(path)

for i, file in enumerate(files):
    old_path = os.path.join(path, file)
    new_name = f"{i+1:03d}_{file}"
    new_path = os.path.join(path, new_name)
    if dry_run :
        print(f"[DRY RUN] {old_path} -> {new_path}")
    else :
        os.rename(old_path, new_path)

print("완료")
