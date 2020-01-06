#!/usr/bin/env python

import tkinter as tk
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
                indicatoron=0
            ).grid(column=1, row=i+1, sticky=[tk.W, tk.E])

    def getSelectedVar(self):
        return self.selectedVar


class Quiz(tk.Frame):
    def __init__(self, master, backend, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.backend = backend
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
        self.questionFrame.setAnswers(
            self.backend.getAnswers()
        )
        self.questionFrame.populateQuestion()
        self.questionFrame.grid(row=0, columnspan=2, sticky=[tk.W, tk.E])

    def submitAnswer(self):
        answerIndex = self.selectedVar.get()
        correct = self.backend.checkAnswerByString(backend.getAnswers()[answerIndex])
        if correct:
            messagebox.showinfo(message="Correct!")
        else:
            messagebox.showinfo(message="Unfortunately not")
        try:
            self.backend.nextQuestion()
            self.questionFrame.destroy()
            self.populateQuestionFrame()
        except QuizOverException:
            messagebox.showinfo(message="The quiz is over. Thank you.")
            self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Quiz")
    backend = QuizBackend()
    quiz = Quiz(master=root, backend=backend)
    quiz.mainloop()
