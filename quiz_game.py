import json

from quiz import Quiz, DEFAULT_QUIZZES


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.loaded_from_file = False
        self.load_state()

    def load_state(self):
        try:
            with open("state.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            self.quizzes = []
            for q in data["quizzes"]:
                self.quizzes.append(Quiz(q["question"], q["choices"], q["answer"]))
            self.best_score = data["best_score"]
            self.loaded_from_file = True

        except FileNotFoundError:
            # 첫 실행: state.json이 아직 없음
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = 0
            self.loaded_from_file = False

        except (json.JSONDecodeError, KeyError, TypeError):
            # JSONDecodeError: JSON 문법이 깨진 경우
            # KeyError: 필요한 키("quizzes", "best_score" 등)가 없는 경우
            # TypeError: 값의 타입이 잘못된 경우 (예: quizzes가 리스트가 아님)
            print("저장된 데이터가 손상되었습니다. 기본 데이터로 복구합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = 0
            self.loaded_from_file = False

    def save_state(self):
        data = {
            "quizzes": [],
            "best_score": self.best_score,
        }
        for quiz in self.quizzes:
            data["quizzes"].append({
                "question": quiz.question,
                "choices": quiz.choices,
                "answer": quiz.answer,
            })

        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def show_menu(self):
        print("========================================")
        print("        나만의 퀴즈 게임")
        print("========================================")

        if self.loaded_from_file:
            count = len(self.quizzes)
            score = self.best_score
            print(f"저장된 데이터를 불러왔습니다. (퀴즈 {count}개, 최고점수 {score}점)")
            print("========================================")
            self.loaded_from_file = False

        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("========================================")

    def get_menu_choice(self):
        while True:
            try:
                user_input = input("선택: ").strip()
                choice = int(user_input)
                if 1 <= choice <= 5:
                    return choice
                print("잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            except ValueError:
                # 빈 입력이나 숫자가 아닌 문자열을 int()로 변환 시 발생
                print("잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = self.get_menu_choice()

                if choice == 1:
                    print("\n아직 구현되지 않은 기능입니다.\n")
                elif choice == 2:
                    print("\n아직 구현되지 않은 기능입니다.\n")
                elif choice == 3:
                    print("\n아직 구현되지 않은 기능입니다.\n")
                elif choice == 4:
                    print("\n아직 구현되지 않은 기능입니다.\n")
                elif choice == 5:
                    print("\n게임을 종료합니다.")
                    break

        except (KeyboardInterrupt, EOFError):
            # KeyboardInterrupt: Ctrl+C 입력 시 발생
            # EOFError: Ctrl+D 입력 시 발생
            print("\n\n게임을 종료합니다.")
