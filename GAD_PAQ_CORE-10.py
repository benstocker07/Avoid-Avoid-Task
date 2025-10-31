def administer_questionnaire(name, questions, scale_desc, valid_range):
    print(f"\n{name} — {scale_desc}")
    answers = []
    for i, question in enumerate(questions, 1):
        while True:
            try:
                response = int(input(f"{i}. {question} "))
                if response in valid_range:
                    answers.append(response)
                    break
                else:
                    print(f"Please enter a number in {valid_range}.")
            except ValueError:
                print("Invalid input. Enter a number.")
    return sum(answers)

# Scoring interpretation functions
def interpret_gad(score):
    if score <= 4: return "Minimal anxiety"
    elif score <= 9: return "Mild anxiety"
    elif score <= 14: return "Moderate anxiety"
    else: return "Severe anxiety"

def interpret_phq9(score):
    if score <= 4: return "Minimal depression"
    elif score <= 9: return "Mild depression"
    elif score <= 14: return "Moderate depression"
    elif score <= 19: return "Moderately severe depression"
    else: return "Severe depression"

def interpret_core10(score):
    if score <= 5: return "Healthy"
    elif score <= 10: return "Low-level distress"
    elif score <= 15: return "Mild distress"
    elif score <= 20: return "Moderate distress"
    elif score <= 25: return "Moderately severe distress"
    else: return "Severe distress"

# Questions
gad7_questions = [
    "Feeling nervous, anxious or on edge?",
    "Not being able to stop or control worrying?",
    "Worrying too much about different things?",
    "Trouble relaxing?",
    "Being so restless that it is hard to sit still?",
    "Becoming easily annoyed or irritable?",
    "Feeling afraid as if something awful might happen?"
]

phq9_questions = [
    "Little interest or pleasure in doing things?",
    "Feeling down, depressed, or hopeless?",
    "Trouble falling or staying asleep, or sleeping too much?",
    "Feeling tired or having little energy?",
    "Poor appetite or overeating?",
    "Feeling bad about yourself — or that you are a failure or have let yourself or your family down?",
    "Trouble concentrating on things?",
    "Moving or speaking slowly or being very fidgety?",
    "Thoughts that you would be better off dead or hurting yourself?"
]

core10_questions = [
    "I have felt terribly alone and isolated",
    "I have felt tense, anxious or nervous",
    "I have felt I have someone to turn to for support when needed",
    "I have felt able to cope when things go wrong",
    "I have been troubled by aches, pains or other physical problems",
    "I have been feeling unhappy",
    "Talking to people has felt too much for me",
    "I have felt optimistic about my future",
    "I have achieved the things I wanted to",
    "I have felt humiliated or shamed by other people"
]

# Administer and score
gad7_score = administer_questionnaire("GAD-7", gad7_questions, "0 = Not at all, 3 = Nearly every day", range(0, 4))
print(f"GAD-7 Score: {gad7_score} — {interpret_gad(gad7_score)}")

phq9_score = administer_questionnaire("PHQ-9", phq9_questions, "0 = Not at all, 3 = Nearly every day", range(0, 4))
print(f"PHQ-9 Score: {phq9_score} — {interpret_phq9(phq9_score)}")

core10_score = administer_questionnaire("CORE-10", core10_questions, "0 = Not at all, 4 = Most or all of the time", range(0, 5))
print(f"CORE-10 Score: {core10_score} — {interpret_core10(core10_score)}")
