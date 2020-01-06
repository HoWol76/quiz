class QuizOverException(Exception):
    def __init__(self):
        super().__init__()

class QuizBackend():
    def __init__(self, frontend):
        self.frontend = frontend

    def getQuestion(self):
        return "What is 2+2"

    def getAnswers(self):
        return [str(i) for i in range(1, 5)]

    def checkAnswerByString(self, answer):
        return answer == "4"

    def checkAnswerByIndex(self, answerIndex):
        return answer == 3

    def nextQuestion(self):
        raise QuizOverException()
