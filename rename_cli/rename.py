import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="파일 이름 정리 도구")
    parser.add_argument("--path", required=True, help="정리할 폴더 경로")
    parser.add_argument("--dry-run", action="store_true", help="실제 변경 없이 미리보기 출력")
    return parser.parse_args()

def build_plan(path, files):
    plan = []
    for i, file in enumerate(files):
        old_path = os.path.join(path, file)
        new_name = f"{i+1:03d}_{file}"
        new_path = os.path.join(path, new_name)
        plan.append((old_path, new_path))
    return plan

def main():
    args = parse_args()
    path = args.path
    dry_run = args.dry_run

    files = sorted(os.listdir(path))

    plan = build_plan(path, files)

    for old_path, new_path in plan:
        if dry_run:
            print(f"[DRY RUN] {old_path} -> {new_path}")
        else:
            os.rename(old_path, new_path)


if __name__ == "__main__":
    main()
