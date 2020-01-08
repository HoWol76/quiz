#!/usr/bin/env python

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
from quizBackend import QuizBackend, QuizOverException

class QuestionFrame(tk.Frame):
    def __init__(self, master=None, selectedVar=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        if selectedVar:
            self.selectedVar = selectedVar
        else:
            self.selectedVar = tk.IntVar()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

    def setQuestion(self, question):
        self.question = question

    def setAnswers(self, answers):
        self.answers = answers

    def populateQuestion(self):
        tk.Label(self,
            text = self.question
        ).grid(row=0, column=0, columnspan=2, sticky=[tk.W, tk.E])
        for i, ans in enumerate(self.answers):
            tk.Radiobutton(
                self,
                text=ans,
                variable=self.selectedVar,
                value=i,
                indicatoron=0,
                command=self.master.submitAnswer
            ).grid(column=1, row=i+1, sticky=[tk.W, tk.E])

    def getSelectedVar(self):
        return self.selectedVar


class Quiz(tk.Frame):
    def __init__(self, master, backend, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.backend = backend
        self.defaultFont = tkfont.nametofont('TkDefaultFont')
        self.defaultFont.configure(size=16)
        self.selectedVar = tk.IntVar()
        self.populateWindow()
        self.master.title("Quiz")
        self.master.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky=[tk.W, tk.E])

    def populateWindow(self):

        # Submit Button
        tk.Button(
            self,
            text="Submit", bg="green",
            command=self.submitAnswer
        ).grid(row=1, column=0, sticky=[tk.W, tk.E], padx=10, pady=5)
        # Quit Button
        tk.Button(
            self,
            text="Quit", bg="red",
            command=self.master.destroy
        ).grid(row=1, column=1, sticky=[tk.W, tk.E], padx=10, pady=5)

        self.populateQuestionFrame()

    def populateQuestionFrame(self):
        self.selectedVar.set(-1)
        self.questionFrame = QuestionFrame(master=self, selectedVar=self.selectedVar)
        self.questionFrame.setQuestion(
            self.backend.getQuestion()
        )
        self.answers = self.backend.getAnswers()
        self.questionFrame.setAnswers(self.answers)
        self.questionFrame.populateQuestion()
        self.questionFrame.grid(row=0, columnspan=2, sticky=[tk.W, tk.E])

    def submitAnswer(self):
        answerIndex = self.selectedVar.get()
        correct = self.backend.checkAnswerByString(self.answers[answerIndex])
        if correct:
            messagebox.showinfo(message="Correct!")
        else:
            messagebox.showinfo(message="Unfortunately not")
        try:
            self.backend.nextQuestion()
            self.questionFrame.destroy()
            self.populateQuestionFrame()
        except QuizOverException:
            totals = self.backend.getTotals()
            messagebox.showinfo(message=f"The quiz is over. Thank you.\nYou got {totals['correct']} of {totals['total']}")
            self.master.destroy()


class QuizCMD():

    def __init__(self, backend):
        self.__backend = backend

    def mainloop(self):
        from string import ascii_letters as letters
        while True:
            print(backend.getQuestion())
            answers = {l: a for l, a in zip(letters, backend.getAnswers())}
            for l, a in answers.items():
                print(f" {l}) {a}")
            answerGiven = input(f"Please enter answer {list(answers.keys())}")
            if backend.checkAnswerByString(answers[answerGiven]):
                print("Correct!")
            else:
                print("No, Sorry")
            try:
                backend.nextQuestion()
            except QuizOverException:
                break

        totals = self.__backend.getTotals()
        print(f"You got {totals['correct']} of {totals['total']} questions right.")


def main():
    backend = QuizBackend(file='questions.yaml')

    # Check for Tcl/Tk availability
    try:
        root = tk.Tk()
        tkAvailable = True
    except tk.TclError:
        tkAvailable = False

    # Select correct User Interface
    if tkAvailable:
        root.title("Quiz")
        quiz = Quiz(master=root, backend=backend)
    else:
        quiz = QuizCMD(backend=backend)

    # Run the quiz
    quiz.mainloop()


if __name__ == '__main__':
    main()
