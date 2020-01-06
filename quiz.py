#!/usr/bin/env python

import tkinter as tk
from tkinter import messagebox

from quizBackend import QuizBackend, QuizOverException

class Quiz(tk.Frame):
    def __init__(self, master, backend):
        super().__init__(master)
        self.master = master
        self.backend = backend
        self.questionFrame = None
        self.populateWindow()
        self.master.title("Quiz")
        self.pack()

    def populateWindow(self):
        self.getQuestionFrame()

        # Submit Button
        tk.Button(
            self,
            text="Submit", bg="green",
            command=self.submitAnswer
        ).pack()
        # Quit Button
        tk.Button(
            self,
            text="Quit", bg="red",
            command=self.master.destroy
        ).pack()

    def getQuestionFrame(self):
        self.questionFrame = tk.Frame(self)
        self.answerSelectedIndex = tk.IntVar()
        tk.Label(self.questionFrame,
            text = self.backend.getQuestion()
        ).pack()
        for i, ans in enumerate(self.backend.getAnswers()):
            tk.Radiobutton(
                self.questionFrame,
                text=ans,
                variable=self.answerSelectedIndex,
                value=i,
                indicatoron=0
            ).pack()
        self.questionFrame.pack()

    def submitAnswer(self):
        answerIndex = self.answerSelectedIndex.get()
        print(f"Selected answer index: {answerIndex}")
        correct = self.backend.checkAnswerByIndex(answerIndex)
        if correct:
            messagebox.showinfo(message="Correct!")
        else:
            messagebox.showinfo(message="Unfortunately not")
        try:
            self.backend.nextQuestion()
        except QuizOverException:
            messagebox.showinfo(message="The quiz is over. Thank you.")
            self.master.destroy()




if __name__ == '__main__':
    root = tk.Tk()
    backend = QuizBackend()
    quiz = Quiz(master=root, backend=backend)
    quiz.mainloop()
