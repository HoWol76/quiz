class QuizOverException(Exception):
    def __init__(self):
        super().__init__()

class QuizBackend():
    def __init__(self):
        self.num_questions = 1
        self.active_question = 0

    def getQuestion(self):
        return "What is 2+2"

    def getAnswers(self):
        return [str(i) for i in range(1, 5)]

    def checkAnswerByString(self, answer):
        return answer == "4"

    def checkAnswerByIndex(self, answerIndex):
        return answer == 3

    def nextQuestion(self):
        self.active_question = self.active_question + 1
        if self.active_question >= self.num_questions:
            raise QuizOverException()
