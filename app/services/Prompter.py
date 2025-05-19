from .Prompt_Result import Prompt_Result, Prompt_Results
from typing import TypeVar
TOptions = TypeVar('TOptions')


# Only one answer
def prompt(options: list[TOptions], trials: int = 3, input_text = "> "):
    result = Prompt_Result[TOptions](None)
    for _ in range(trials):
        temp: str = input(input_text).strip().capitalize()
        if len(temp) != 1:
            print(f"Give a valid answer!")
            continue
        answer_idx: int = ord(temp) - 65
        if answer_idx in range(len(options)):
            return result.configure(value = options[answer_idx], index = answer_idx)
        else:
            print(f"Prompt only from A to {chr(65 + len(options) - 1)}!")
            continue
    return result.configure(err_val = temp, crashed = True, message = f"Invalid answer {trials} times!")

# Can have multiple answers        
def prompt_multiple(options: list[TOptions], count_correct: int, trials: int = 3):
    result = Prompt_Results[TOptions]()
    print(f"Prompt {count_correct} answers:")
    for i in range(count_correct):
        prompt_result = prompt(options, trials, f"Answer #{i + 1}> ")
        if prompt_result.crashed:
            return result.configure(err_val = prompt_result.err_val, crashed = True, message = f"Invalid answer {trials} times!")
        result.values.append(prompt_result.value)
        result.indexes.append(prompt_result.index)
    return result

# Can prompt int
def prompt_int(options: list[int], trials: int = 3, input_text = "> ") -> Prompt_Result[int]:
    result = Prompt_Result[int](None)
    for _ in range(trials):
        try:
            temp = input(input_text).strip()
            answer_idx: int = int(temp)
        except ValueError:
            print(f"Give a valid answer!")
            continue
        else:
            result.configure(value = options[answer_idx], index = answer_idx)
    return result.configure(err_val = temp, crashed = True, message = f"Invalid answer {trials} times!")

# Can prompt int or multiple choices
def prompt_multiple_int(options: list[TOptions], count_correct: int, trials: int = 3):
    result = Prompt_Results[TOptions]()
    print(f"Prompt {count_correct} answers:")
    for i in range(count_correct):
        try:
            temp = input(f"Answer #{i + 1}> ").strip().capitalize()
            answer_idx: int = int(temp)
            return Prompt_Result(None, -1, message = "int", err_val = answer_idx)
        except ValueError:
            if len(temp) != 1:
                print(f"Give a valid answer!")
                continue
            
            answer_idx: int = ord(temp) - 65
            if answer_idx in range(len(options)):
                prompt_result = result.configure(value = options[answer_idx], index = answer_idx, message = "obj")
            else:
                print(f"Prompt only from A to {chr(65 + len(options) - 1)}!")
                continue
            
            result.values.append(prompt_result.value)
            result.indexes.append(prompt_result.index)     
        
    if len(result.indexes) != count_correct:
        return result.configure(crashed = True, message = f"Invalid answer {trials} times!")
    return result