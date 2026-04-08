import json
import random
from datetime import datetime

from quiz import Quiz, DEFAULT_QUIZZES


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = {"score": 0, "correct": 0, "total": 0}
        self.has_played = False
        self.history = []
        self.loaded_from_file = False
        self.load_state()

    def load_state(self):
        try:
            with open("state.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            self.quizzes = []
            for q in data["quizzes"]:
                self.quizzes.append(Quiz(q["question"], q["choices"], q["answer"], q["hint"]))
            self.best_score = data["best_score"]
            self.has_played = data["has_played"]
            self.history = data["history"]
            self.loaded_from_file = True

        except FileNotFoundError:
            # 첫 실행: state.json이 아직 없음
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = {"score": 0, "correct": 0, "total": 0}
            self.history = []
            self.loaded_from_file = False

        except (json.JSONDecodeError, KeyError, TypeError):
            # JSONDecodeError: JSON 문법이 깨진 경우
            # KeyError: 필요한 키("quizzes", "best_score" 등)가 없는 경우
            # TypeError: 값의 타입이 잘못된 경우 (예: quizzes가 리스트가 아님)
            print("저장된 데이터가 손상되었습니다. 기본 데이터로 복구합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = {"score": 0, "correct": 0, "total": 0}
            self.has_played = False
            self.history = []
            self.loaded_from_file = False
            self.save_state()

    def save_state(self):
        data = {
            "quizzes": [],
            "best_score": self.best_score,
            "has_played": self.has_played,
            "history": self.history,
        }
        for quiz in self.quizzes:
            data["quizzes"].append({
                "question": quiz.question,
                "choices": quiz.choices,
                "answer": quiz.answer,
                "hint": quiz.hint,
            })

        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def show_menu(self):
        print("========================================")
        print("        나만의 퀴즈 게임")
        print("========================================")

        if self.loaded_from_file:
            count = len(self.quizzes)
            score = self.best_score["score"]
            print(f"저장된 데이터를 불러왔습니다. (퀴즈 {count}개, 최고점수 {score}점)")
            print("========================================")
            self.loaded_from_file = False

        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")
        print("========================================")

    def _get_number_in_range(self, prompt, low, high):
        while True:
            try:
                user_input = input(prompt).strip()
                choice = int(user_input)
                if low <= choice <= high:
                    return choice
                print(f"잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            except ValueError:
                print(f"잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")

    def _get_nonempty_input(self, prompt, error_message):
        while True:
            user_input = input(prompt).strip()
            if user_input:
                return user_input
            print(error_message)

    def get_menu_choice(self):
        return self._get_number_in_range("선택: ", 1, 6)

    def _ask_single_question(self, quiz, question_number):
        print()
        print("----------------------------------------")
        quiz.display(question_number)
        print()

        hint_used = False

        while True:
            try:
                user_input = input("정답 입력 (h=힌트): ").strip()

                if user_input.lower() == "h":
                    if quiz.hint:
                        print(f"힌트: {quiz.hint}")
                        hint_used = True
                    else:
                        print("이 문제에는 힌트가 없습니다.")
                    continue

                answer = int(user_input)
                if 1 <= answer <= 4:
                    break
                print("잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
            except ValueError:
                print("잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")

        if quiz.check_answer(answer):
            print("정답입니다!")
            if hint_used:
                print("(힌트를 사용하여 절반만 인정)")
                return 0.5
            return 1
        else:
            print(f"틀렸습니다. 정답은 {quiz.answer}번입니다.")
            return 0

    def _record_result(self, total, correct_count, score):
        print()
        print("========================================")
        print(f"결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")

        self.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total": total,
            "correct": correct_count,
            "score": score,
        })

        if not self.has_played or score > self.best_score["score"]:
            self.has_played = True
            print("새로운 최고 점수입니다!")
            self.best_score = {
                "score": score,
                "correct": correct_count,
                "total": total,
            }

        self.save_state()

        print("========================================")

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        total_available = len(self.quizzes)
        print(f"퀴즈를 시작합니다! (총 {total_available}문제 중 몇 문제를 풀겠습니까?)")
        count = self._get_number_in_range(f"문제 수 입력 (1-{total_available}): ", 1, total_available)
        selected_quizzes = random.sample(self.quizzes, count)

        print(f"\n{count}문제를 풀겠습니다!")

        correct_count = 0
        for i, quiz in enumerate(selected_quizzes):
            correct_count += self._ask_single_question(quiz, i + 1)

        score = int(correct_count / count * 100)
        self._record_result(count, correct_count, score)

    def add_quiz(self):
        print("새로운 퀴즈를 추가합니다.")
        print()

        question = self._get_nonempty_input("문제를 입력하세요: ", "문제를 입력해주세요.")

        choices = []
        for i in range(1, 5):
            choice = self._get_nonempty_input(f"선택지 {i}: ", "선택지를 입력해주세요.")
            choices.append(choice)

        answer = self._get_number_in_range("정답 번호 (1-4): ", 1, 4)
        hint = input("힌트 (없으면 Enter): ").strip()

        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.save_state()
        print()
        print("퀴즈가 추가되었습니다!")

    def show_quiz_list(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        total = len(self.quizzes)
        print(f"등록된 퀴즈 목록 (총 {total}개)")
        print()
        print("----------------------------------------")
        for i, quiz in enumerate(self.quizzes):
            print(f"[{i + 1}] {quiz.question}")
        print("----------------------------------------")

    def show_score(self):
        if not self.has_played:
            print("아직 퀴즈를 풀지 않았습니다.")
            return

        score = self.best_score["score"]
        correct = self.best_score["correct"]
        total = self.best_score["total"]
        print(f"최고 점수: {score}점 ({total}문제 중 {correct}문제 정답)")

        if self.history:
            print()
            print("게임 기록:")
            print("----------------------------------------")
            for i, record in enumerate(self.history):
                date = record["date"]
                r_total = record["total"]
                r_correct = record["correct"]
                r_score = record["score"]
                print(f"[{i + 1}] {date} | {r_total}문제 중 {r_correct}문제 정답 ({r_score}점)")
            print("----------------------------------------")

    def delete_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        self.show_quiz_list()
        print()

        total = len(self.quizzes)
        choice = self._get_number_in_range(f"삭제할 퀴즈 번호 (1-{total}, 취소=0): ", 0, total)
        if choice == 0:
            print("삭제를 취소했습니다.")
            return

        deleted = self.quizzes.pop(choice - 1)
        self.save_state()
        print(f"퀴즈가 삭제되었습니다: {deleted.question}")

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = self.get_menu_choice()

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quiz_list()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    self.delete_quiz()
                elif choice == 6:
                    print("\n게임을 종료합니다.")
                    break

        except (KeyboardInterrupt, EOFError):
            # KeyboardInterrupt: Ctrl+C 입력 시 발생
            # EOFError: Ctrl+D 입력 시 발생
            print("\n\n게임을 종료합니다.")
