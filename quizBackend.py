class QuizOverException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class QuizBackend():
    def __init__(self, *args, **kwargs):
        self.questions = [
            {
                'question': "What is 2+2",
                'answers': ["1", "2", "3", "4"],
                'correct': 3
            },
            {
                'question': "Who develops Minecraft",
                'answers': ["Konami", "Mojang", "Blizzard", "EA"],
                'correct': 1
            },
        ]
        self.num_questions = len(self.questions)
        self.active_question_num = 0
        self.active_question = self.questions[self.active_question_num]

    def getQuestion(self):
        return self.active_question['question']

    def getAnswers(self):
        return self.active_question['answers']

    def checkAnswerByString(self, answer):
        return answer == self.active_question['answers'][
            self.active_question['correct']
        ]

    def checkAnswerByIndex(self, answerIndex):
        return answerIndex == self.active_question['correct']

    def nextQuestion(self):
        self.active_question_num = self.active_question_num + 1
        if self.active_question_num >= self.num_questions:
            raise QuizOverException()
        self.active_question = self.questions[self.active_question_num]
