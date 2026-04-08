class Quiz:
    def __init__(self, question, choices, answer, hint):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self, number):
        print(f"[문제 {number}]")
        print(self.question)
        print()
        
        i = 1
        for choice in self.choices:
            print(f"{i}. {choice}")
            i += 1

    def check_answer(self, user_answer):
        return user_answer == self.answer


DEFAULT_QUIZZES = [
    Quiz(
        "Python에서 리스트의 마지막 요소에 접근하는 인덱스는?",
        ["0", "-1", "last", "end"],
        2,
        "Python에서 음수 인덱스는 뒤에서부터 셉니다.",
    ),
    Quiz(
        "Python의 창시자는?",
        ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Gosling"],
        1,
        "네덜란드 출신의 프로그래머입니다.",
    ),
    Quiz(
        "컴퓨터가 데이터를 저장하는 가장 작은 단위는?",
        ["바이트(Byte)", "비트(Bit)", "워드(Word)", "니블(Nibble)"],
        2,
        "binary digit의 줄임말입니다.",
    ),
    Quiz(
        "HTTP 상태 코드 404의 의미는?",
        ["서버 오류", "권한 없음", "리다이렉션", "찾을 수 없음"],
        4,
        "Not Found를 한국어로 번역하면?",
    ),
    Quiz(
        "Git에서 변경 사항을 스테이징 영역에 추가하는 명령어는?",
        ["git commit", "git push", "git add", "git pull"],
        3,
        "'추가하다'를 영어로?",
    ),
]
