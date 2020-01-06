class QuizOverException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class QuizBackend():
    def __init__(self, file=None, *args, **kwargs):
        if not file:
            self.questions = [
                {
                    'question': "What is 2+2",
                    'answers': ["1", "2", "3", "4"],
                    'correct': "4"
                },
                {
                    'question': "Who develops Minecraft",
                    'answers': ["Konami", "Mojang", "Blizzard", "EA"],
                    'correct': "Mojang"
                },
            ]
        else:
            import yaml
            with open(file, 'r') as stream:
                self.questions = yaml.load(stream)
        self.answeredCorrectly = False

        self.num_questions = len(self.questions)
        self.active_question_num = 0
        self.num_answeredCorrectly = 0
        self.active_question = self.questions[self.active_question_num]

    def getQuestion(self):
        return self.active_question['question']

    def getAnswers(self):
        return self.active_question['answers']

    def checkAnswerByString(self, answer):
        self.answeredCorrectly = (answer == self.active_question['correct'])
        return self.answeredCorrectly

    def nextQuestion(self):
        self.active_question_num = self.active_question_num + 1
        if self.answeredCorrectly:
            self.num_answeredCorrectly = self.num_answeredCorrectly+1
        if self.active_question_num >= self.num_questions:
            raise QuizOverException()
        self.active_question = self.questions[self.active_question_num]

    def getTotals(self):
        return {
            'correct': self.num_answeredCorrectly,
            'asked': self.active_question_num,
            'total': self.num_questions
        }
