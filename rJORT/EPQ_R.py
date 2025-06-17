import tkinter as tk
from tkinter import messagebox
import random
import sqlite3
import datetime

LIKERT_OPTIONS = [
    "Strongly Disagree",
    "Disagree",
    "Agree",
    "Strongly Agree"
]

STATEMENTS = [
        "Does your mood often go up and down?",
        "Do you take much notice of what people think?",
        "Are you a talkative person?",
        "If you say you will do something, do you always keep your promise no matter how inconvenient it might be?",
        "Do you ever feel ‘just miserable’ for no reason?",
        "Would being in debt worry you?",
        "Are you rather lively?",
        "Were you ever greedy by helping yourself to more than your share of anything?",
        "Are you an irritable person?",
        "Would you take drugs which may have strange or dangerous effects?",
        "Do you enjoy meeting new people?",
        "Have you ever blamed someone for doing something you knew was really your fault?",
        "Are your feelings easily hurt?",
        "Do you prefer to go your own way rather than act by the rules?",
        "Can you usually let yourself go and enjoy yourself at a lively party?",
        "Are all your habits good and desirable ones?",
        "Do you often feel ‘fed-up’?",
        "Do good manners and cleanliness matter much to you?",
        "Do you usually take the initiative in making new friends?",
        "Have you ever taken anything (even a pin or button) that belonged to someone else?",
        "Would you call yourself a nervous person?",
        "Do you think marriage is old-fashioned and should be done away with?",
        "Can you easily get some life into a rather dull party?",
        "Have you ever broken or lost something belonging to someone else?",
        "Are you a worrier?",
        "Do you enjoy co-operating with others?",
        "Do you tend to keep in the background on social occasions?",
        "Does it worry you if you know there are mistakes in your work?",
        "Have you ever said anything bad or nasty about anyone?",
        "Would you call yourself tense or ‘highly-strung’?",
        "Do you think people spend too much time safeguarding their future with savings and insurances?",
        "Do you like mixing with people?",
        "As a child were you ever cheeky to your parents?",
        "Do you worry too long after an embarrassing experience?",
        "Do you try not to be rude to people?",
        "Do you like plenty of bustle and excitement around you?",
        "Have you ever cheated at a game?",
        "Do you suffer from ‘nerves’?",
        "Would you like other people to be afraid of you?",
        "Have you ever taken advantage of someone?",
        "Are you mostly quiet when you are with other people?",
        "Do you often feel lonely?",
        "Is it better to follow society’s rules than go your own way?",
        "Do other people think of you as being very lively?",
        "Do you always practice what you preach?",
        "Are you often troubled about feelings of guilt?",
        "Do you sometimes put off until tomorrow what you ought to do today?",
        "Can you get a party going?"
    ]
fontsize = 16

original_order = STATEMENTS.copy()
random.shuffle(STATEMENTS)

class LikertSurveyApp:
    def save_to_sqlite(self):
        conn = sqlite3.connect("rJORT.db")
        cursor = conn.cursor()

        num_questions = len(STATEMENTS)
        columns = ", ".join([f"Q{i+1} INTEGER" for i in range(num_questions)])

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS EPQ_r (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                {columns}
            )
        """)

        timestamp = datetime.datetime.now().isoformat()

        responses_ordered = []
        for i in range(num_questions):
            question = STATEMENTS[i]
            score = self.responses.get(question, 0) 
            responses_ordered.append(score)

        placeholders = ", ".join(["?"] * (num_questions + 1))

        cursor.execute(f"INSERT INTO EPQ_r (timestamp, {', '.join([f'Q{i+1}' for i in range(num_questions)])}) VALUES ({placeholders})",
                       (timestamp, *responses_ordered))

        conn.commit()
        conn.close()
        
    def __init__(self, root):
        self.root = root
        self.root.title("Personality Metrics")
        self.root.geometry("700x400")
        self.root.resizable(False, False)

        self.page_size = 5
        self.current_index = 0
        self.responses = {}

        self.title_label = tk.Label(root, text="Please rate your agreement with the following:", font=("Arial", fontsize+2))
        self.title_label.pack(pady=10)

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.nav_button = tk.Button(root, text="Next", command=self.next_page)
        self.nav_button.pack(pady=10)

        self.draw_page()

    def draw_page(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.vars = []
        for i in range(self.page_size):
            q_index = self.current_index + i
            if q_index >= len(STATEMENTS):
                break

            statement = STATEMENTS[q_index]
            tk.Label(
                self.frame,
                text=statement,
                anchor="w",
                font=("Arial", fontsize),
                justify="left",
                wraplength=400  
            ).grid(row=i, column=0, padx=5, pady=4, sticky="w")

            var = tk.IntVar(value=self.responses.get(statement, 0))
            self.vars.append((statement, var))

            for j, option in enumerate(LIKERT_OPTIONS, 1):
                tk.Radiobutton(self.frame, variable=var, value=j).grid(row=i, column=j, padx=5)

    def next_page(self):
        for statement, var in self.vars:
            if var.get() == 0:
                messagebox.showerror("Incomplete", "Please answer all questions before proceeding.")
                return
            self.responses[statement] = var.get()

        self.current_index += self.page_size
        if self.current_index >= len(STATEMENTS):
            self.finish()
        else:
            self.draw_page()

    def finish(self):
        self.save_to_sqlite()
        messagebox.showinfo("Thank you!", "Your responses have been recorded.")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.update_idletasks()
    width = 600
    height = 400
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.attributes("-topmost", True)

    app = LikertSurveyApp(root)
    root.mainloop()
