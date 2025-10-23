import tkinter as tk
from tkinter import messagebox
import random
import hashlib

questions = [
            "I feel calm",
            "I feel secure",
            "I am tense",
            "I feel strained",
            "I feel at ease",
            "I feel upset",
            "I am presently worrying over possible misfortunes",
            "I feel satisfied",
            "I feel frightened",
            "I feel comfortable",
            "I feel self-confident",
            "I feel nervous",
            "I am jittery",
            "I feel indecisive",
            "I am relaxed",
            "I feel content",
            "I am worried",
            "I feel confused",
            "I feel steady",
            "I feel pleasant",
            "I feel nervous and restless",
            "I feel satisfied with myself",
            "I wish I could be as happy as others seem to be",
            "I feel like a failure",
            "I feel rested",
            "I am 'calm, cool, and collected'",
            "I feel that difficulties are piling up so that I cannot overcome them",
            "I worry too much over something that really doesn't matter",
            "I am happy",
            "I have disturbing thoughts",
            "I lack self-confidence",
            "I feel secure",
            "I make decisions easily",
            "I feel inadequate",
            "I am content",
            "Some unimportant thought runs through my mind and bothers me",
            "I take disappointments so keenly that I can't put them out of my mind",
            "I am a steady person",
            "I get in a state of tension or turmoil as I think about my recent concerns and interests"
]

random.shuffle(questions)

class SurveyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Survey")
        self.root.configure(bg="white")
        self.root.attributes("-topmost",True)
        self.root.iconbitmap(default="")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 800
        window_height = 400
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.answers = [0] * len(questions)
        self.current_question = 0

        self.frame = tk.Frame(root, bg="white")
        self.frame.pack(expand=True, fill="both")

        self.show_intro()

    def show_intro(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        intro_text = "Welcome to the survey!\n\nPlease read the instructions carefully before starting.\nClick anywhere to continue."
        label = tk.Label(self.frame, text=intro_text, bg="white", fg="#333", font=("Arial", 14), wraplength=760, justify="center")
        label.pack(expand=True, padx=20, pady=50)

        self.frame.bind("<Button-1>", self.start_questions)
        self.frame.bind("<Return>", self.start_questions)

    def start_questions(self, event=None):
        self.frame.unbind("<Button-1>")
        self.frame.unbind("<Return>")
        self.show_question()

    def show_question(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        if self.current_question < len(questions):
            tk.Label(self.frame, text=f"{self.current_question+1}. {questions[self.current_question]}",
                     bg="white", fg="#333", font=("Arial", 14, "bold"), wraplength=760, justify="center").pack(expand=True, pady=50)
            tk.Label(self.frame, text="Press keys 1-5 to answer", bg="white", fg="#666", font=("Arial", 14)).pack(pady=20)
            self.root.bind("<Key>", self.key_pressed)
        else:
            self.finish()

    def key_pressed(self, event):
        if event.char in ['1','2','3','4','5']:
            self.answers[self.current_question] = int(event.char)
            self.current_question += 1
            self.show_question()
            sys.exit()

    def finish(self):
        result_text = f"Responses:\n{self.answers}"
        tk.Label(self.frame, text=result_text, bg="white", fg="#333", font=("Arial", 14)).pack(expand=True, pady=50)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SurveyApp(root)
    root.mainloop()
