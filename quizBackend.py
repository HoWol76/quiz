class QuizBackend():
    def __init__(self, frontend):
        self.frontend = frontend

    def getQuestion(self):
        return "What is 2+2"

    def getAnswers(self):
        return [str(i) for i in range(1, 5)]
        
