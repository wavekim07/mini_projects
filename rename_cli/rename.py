import os
import argparse

def parse_args():
    """
    CLI 인자를 파싱한다.
    --path : 정리할 대상 폴더 경로
    --dry-run : 실제 변경 없이 미리보기 모드
    """
    parser = argparse.ArgumentParser(description="파일 이름 정리 도구")
    parser.add_argument("--path", required=True, help="정리할 폴더 경로")
    parser.add_argument("--dry-run", action="store_true", help="실제 변경 없이 미리보기 출력")
    return parser.parse_args()

# 경로/대상 검증(main에서 무조건 1회 호출)
def validate_path(path: str) -> bool:
    # 경로 존재 확인
    if not os.path.exists(path):
        print(f"[ERROR] 경로가 존재하지 않습니다: {path}")
        return False
    # 디렉토리 여부 확인
    if not os.path.isdir(path):
        print(f"[ERROR] 디렉토리 경로를 입력하세요: {path}")
        return False
    
    return True

# 파일 목록을 기반으로 rename 계획(plan)을 생성한다.
def build_plan(path, files):
    # 각 파일에 순번(001_, 002_ ...)을 붙인 새로운 경로를 계산한다.
    plan = []
    for i, file in enumerate(files):
        old_path = os.path.join(path, file)
        new_name = f"{i+1:03d}_{file}"
        new_path = os.path.join(path, new_name)
        plan.append((old_path, new_path))
    return plan
# 생성된 rename 계획을 출력한다.
def print_plan(plan):
    # dry_run 모드에서 사용된다.
    for old_path, new_path in plan:
        print(f"[DRY RUN] {old_path} -> {new_path}")

# rename 계획에 따라 실제 파일 이름을 변경한다.
def apply_plan(plan):
    for old_path, new_path in plan:
        os.rename(old_path, new_path)

# 파일 목록 가져오기(필터링 + 정렬)
def get_files(path: str) -> list[str]:
    return [
        f for f in sorted(os.listdir(path))
        if os.path.isfile(os.path.join(path, f))
    ]

# 프로그램 진입
def main():
    # 인자 파싱 -> 경로 검증 -> 계획 생성 -> 실행/출력 분기 흐름을 담당한다.
    args = parse_args()
    path = args.path
    dry_run = args.dry_run

    # 검증 함수를 무조건 1회 호출
    if not validate_path(path):
        return

    # 파일 목록 함수로 분리
    files = get_files(path)
    
    
    # 파일이 없으면 안전 종료
    if len(files) == 0:
        print(f"[WARN] 처리할 파입이 없습니다: {path}")
        
    plan = build_plan(path, files)

    if dry_run:
        print_plan(plan)
    else:
        apply_plan(plan)


if __name__ == "__main__":
    main()