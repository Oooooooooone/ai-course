import json
import os
from datetime import datetime

# 데이터 파일 경로
DATA_FILE = 'todo.json'

def load_todos():
    """todo.json 파일에서 할 일 목록을 불러옵니다."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_todos(todos):
    """할 일 목록을 todo.json 파일에 저장합니다."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(todos, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")

def add_todo(todos):
    """새로운 할 일을 추가합니다. 마감일도 함께 입력받습니다."""
    task = input("추가할 할 일을 입력하세요: ").strip()
    if not task:
        print("할 일은 빈 칸일 수 없습니다.")
        return

    deadline_str = input("마감일을 입력하세요 (예: YYYY-MM-DD, 없으면 엔터): ").strip()
    
    deadline = None
    if deadline_str:
        try:
            # 입력 형식이 맞는지 확인하기 위해 datetime 객체로 변환 시도
            datetime.strptime(deadline_str, '%Y-%m-%d')
            deadline = deadline_str
        except ValueError:
            print("날짜 형식이 잘못되었습니다 (YYYY-MM-DD 형식 사용). 마감일 없이 추가합니다.")
            deadline = None

    todos.append({
        "task": task, 
        "completed": False,
        "deadline": deadline
    })
    save_todos(todos)
    print(f"'{task}'(이)가 추가되었습니다.")

def list_todos(todos):
    """할 일 목록을 마감일이 빠른 순서대로 보여줍니다."""
    if not todos:
        print("\n현재 할 일이 없습니다.")
        return []

    # 마감일 기준으로 정렬 (마감일이 없는 것은 맨 뒤로)
    def get_deadline_key(todo):
        if todo.get('deadline'):
            try:
                return datetime.strptime(todo['deadline'], '%Y-%m-%d')
            except ValueError:
                return datetime.max
        return datetime.max

    sorted_todos = sorted(todos, key=get_deadline_key)

    print("\n--- 할 일 목록 (마감일 순) ---")
    for i, todo in enumerate(sorted_todos, 1):
        status = "[V]" if todo['completed'] else "[ ]"
        deadline_display = f" | 마감: {todo['deadline']}" if todo.get('deadline') else ""
        print(f"{i}. {status} {todo['task']}{deadline_display}")
    print("------------------------------")
    return sorted_todos

def complete_todo(todos):
    """할 일을 완료 표시합니다."""
    sorted_todos = list_todos(todos)
    if not sorted_todos:
        return

    try:
        idx_in_sorted = int(input("완료 처리할 번호를 입력하세요: ")) - 1
        if 0 <= idx_in_sorted < len(sorted_todos):
            target_todo = sorted_todos[idx_in_sorted]
            target_todo['completed'] = True
            save_todos(todos)
            print(f"'{target_todo['task']}'(이)가 완료되었습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

def delete_todo(todos):
    """할 일을 삭제합니다."""
    sorted_todos = list_todos(todos)
    if not sorted_todos:
        return

    try:
        idx_in_sorted = int(input("삭제할 번호를 입력하세요: ")) - 1
        if 0 <= idx_in_sorted < len(sorted_todos):
            target_todo = sorted_todos[idx_in_sorted]
            todos.remove(target_todo)
            save_todos(todos)
            print(f"'{target_todo['task']}'(이)가 삭제되었습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

def main():
    """메인 메뉴 루프입니다."""
    todos = load_todos()

    while True:
        print("\n=== 할 일 관리 프로그램 ===")
        print("1. 할 일 추가")
        print("2. 목록 보기")
        print("3. 완료 표시")
        print("4. 삭제")
        print("5. 종료")
        choice = input("원하는 메뉴 번호를 선택하세요: ").strip()

        if choice == '1':
            add_todo(todos)
        elif choice == '2':
            list_todos(todos)
        elif choice == '3':
            complete_todo(todos)
        elif choice == '4':
            delete_todo(todos)
        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 시도해주세요.")

if __name__ == "__main__":
    main()
