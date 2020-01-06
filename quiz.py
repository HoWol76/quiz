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

    def setQuestion(self, question):
        self.question = question

    def setAnswers(self, answers):
        self.answers = answers

    def populateQuestion(self):
        tk.Label(self,
            text = self.question
        ).grid()
        for i, ans in enumerate(self.answers):
            tk.Radiobutton(
                self,
                text=ans,
                variable=self.selectedVar,
                value=i,
                indicatoron=0
            ).grid()

    def getSelectedVar(self):
        return self.selectedVar


class Quiz(tk.Frame):
    def __init__(self, master, backend, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.backend = backend
        self.selectedVar = tk.IntVar()
        self.questionFrame = QuestionFrame(master=self, selectedVar=self.selectedVar)
        self.populateWindow()
        self.master.title("Quiz")
        self.grid()

    def populateWindow(self):

        self.questionFrame.setQuestion(
            self.backend.getQuestion()
        )
        self.questionFrame.setAnswers(
            self.backend.getAnswers()
        )
        self.questionFrame.populateQuestion()
        self.questionFrame.grid()

        # Submit Button
        tk.Button(
            self,
            text="Submit", bg="green",
            command=self.submitAnswer
        ).grid()
        # Quit Button
        tk.Button(
            self,
            text="Quit", bg="red",
            command=self.master.destroy
        ).grid()

    def submitAnswer(self):
        answerIndex = self.selectedVar.get()
        print(f"Selected answer index: {answerIndex}")
        correct = self.backend.checkAnswerByIndex(answerIndex)
        if correct:
            messagebox.showinfo(message="Correct!")
        else:
            messagebox.showinfo(message="Unfortunately not")
        try:
            self.backend.nextQuestion()
            self.questionFrame.destroy()
            self.questionFrame = QuestionFrame(master=self, selectedVar = self.selectedVar)
            self.questionFrame.setQuestion(
                self.backend.getQuestion()
            )
            self.questionFrame.setAnswers(
                self.backend.getAnswers()
            )
            self.questionFrame.populateQuestion()
            self.questionFrame.grid()
        except QuizOverException:
            messagebox.showinfo(message="The quiz is over. Thank you.")
            self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    backend = QuizBackend()
    quiz = Quiz(master=root, backend=backend)
    quiz.mainloop()
