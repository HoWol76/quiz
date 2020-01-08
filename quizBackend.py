from random import shuffle


class QuizOverException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class QuizBackend():
    def __init__(self, file=None, *args, **kwargs):
        if not file:
            self.__questions = [
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
                self.__questions = yaml.load(stream)
        self.__answeredCorrectly = False

        self.__num_questions = len(self.__questions)
        self.__active_question_num = 0
        self.__num_answeredCorrectly = 0
        self.__active_question = self.__questions[self.__active_question_num]

    def getQuestion(self):
        """(None) -> str

        Returns the current question text.
        """
        return self.__active_question['question']

    def getAnswers(self):
        """(None) -> list of str

        Returns a shuffled list of answers for the current question
        """
        self.__answers = self.__active_question['answers']
        shuffle(self.__answers)
        self.__correctAnswerIndex = self.__answers.index(self.__active_question['correct'])
        return self.__active_question['answers']

    def checkAnswerByString(self, answer):
        """(str) -> bool

        Returns True if answer contains the correct answer for the current question.

        Side-Effect: Next time /nextQuestion/ is called,
        it will count the question answered correctly if the last
        checkAnswer (either by String or by Index) was correct.
        """
        # print(f"Selected answer: {answer}")
        self.__answeredCorrectly = (answer == self.__active_question['correct'])
        return self.__answeredCorrectly

    def checkAnswerByIndex(self, answerIndex):
        """(int) -> bool

        Returns True if answerIndex contains the index of the correct answer
        in the list last given when /getAnswers/ was called.

        Side-Effect: Next time /nextQuestion/ is called,
        it will count the question answered correctly if the last
        checkAnswer (either by String or by Index) was correct.
        """
        # print(f"Selected answer: {self.__answers[answerIndex]}")
        self.__answeredCorrectly = (answerIndex == self.__correctAnswerIndex)
        return self.__answeredCorrectly

    def nextQuestion(self):
        """(None) -> None

        Activates the next question

        Checks whether the last question was answered correctly by the *last*
        call to /checkAnswerByIndex/ or /checkAnswerByString/. If it was, it will
        increment the tally of questions answered correctly.
        """
        self.__active_question_num = self.__active_question_num + 1
        if self.__answeredCorrectly:
            self.__num_answeredCorrectly = self.__num_answeredCorrectly+1
        if self.__active_question_num >= self.__num_questions:
            raise QuizOverException()
        self.__active_question = self.__questions[self.__active_question_num]

    def getTotals(self):
        """(None) -> dict of {str: int}

        Returns a dictionary of totals:

            key   |  value
        "correct" |  Number of correct answers
        "asked"   |  Number of questions asked so far
        "total"   |  Number of question in this quiz
        """
        return {
            'correct': self.__num_answeredCorrectly,
            'asked': self.__active_question_num,
            'total': self.__num_questions
        }
