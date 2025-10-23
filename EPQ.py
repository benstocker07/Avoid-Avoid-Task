import tkinter as tk
from tkinter import messagebox
import random

questions = [
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

random.shuffle(questions)

class QuestionnaireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Questionnaire")
        self.root.configure(bg="white")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 800
        window_height = 400
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.answers = [0] * len(questions)
        self.current_question = 0

        self.label = tk.Label(root, text="", bg="white", fg="#333", font=("Arial", 18, "bold"), wraplength=760, justify="center")
        self.label.pack(expand=True)

        self.instr = tk.Label(root, text="Press keys 1-5 to answer", bg="white", fg="#666", font=("Arial", 14))
        self.instr.pack(pady=20)

        root.bind("<Key>", self.key_pressed)
        self.show_question()

    def show_question(self):
        if self.current_question < len(questions):
            self.label.config(text=f"{self.current_question+1}. {questions[self.current_question]}")
        else:
            self.finish()

    def key_pressed(self, event):
        if event.char in ['1','2','3','4','5']:
            self.answers[self.current_question] = int(event.char)
            self.current_question += 1
            self.show_question()
            
            with open("Backup/EPQ.csv", mode="a+", newline="") as file:
                file.write('1' + ',' + event.char + ',' + questions[self.current_question] + '\n')

    def finish(self):
        messagebox.showinfo("Results", f"Thank you! Your responses:\n{self.answers}")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestionnaireApp(root)
    root.mainloop()
