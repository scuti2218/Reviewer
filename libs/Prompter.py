from .Question import Question
from .Enums import ChoiceOption


def prompt_answer(question: Question):
    correct_answers: list[str] = [question.data[correct_index].value for correct_index in question.correct_indexes]
    answers_idx: list[int] = []
    answers_correctness: list[bool] = []
    if question.correct_length > 1:
        print(f"Prompt {question.correct_length} answers:")
    for i in range(question.correct_length):
        while True:
            temp: str = input(f"{["", f"Answer #{i + 1} "][question.correct_length > 1]}> ").strip()
            if ChoiceOption.A in question.choice_options:
                temp = temp.capitalize()
                if len(temp) != 1:
                    print(f"Give a valid answer!")
                    continue
                
                answer_idx: int = ord(temp) - 65
                if answer_idx in range(question.length):
                    if answer_idx not in answers_idx:
                        answers_idx.append(answer_idx)
                        answers_correctness.append(question.get_answer_in_randomized(answer_idx).is_correct)
                        break
                    else:
                        print(f"Choose a different answer!")
                else:
                    print(f"Prompt only from A to {chr(question.length - 1)}!")
            else:
                answers_correctness.append(temp in correct_answers)
                break
    return all(answers_correctness)
    
def prompt(options: list[str]):
    while True:
        temp: str = input("> ").strip().capitalize()
        if temp == "":
            print(f"Give an answer!")
            continue
            
        answer_idx: int = ord(temp) - 65
        if answer_idx in range(len(options)):
            return answer_idx
        else:
            print(f"Prompt only from A to {chr(65 + len(options) - 1)}!")