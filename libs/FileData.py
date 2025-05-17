import json
from .Topic import Topic
from os import listdir
from os.path import join as path_join, isdir, exists
from .Question import Question
from .Question_List import Question_List
from .Answer import Answer

def get_data(dir: str) -> Question_List:
    filepath: str = path_join(dir, "index.json")
    with open(filepath, 'r', encoding='utf-8') as file:
        data : list[dict[str, str | list[str]]] = json.load(file)
    return create_question_list(data)

        
def create_question_list(raw_questions: list[dict[str, str | list[str]]]) -> Question_List:
    questions : Question_List = Question_List()
    for raw_question in raw_questions:
        question : Question = Question()
        question.set_value(raw_question["question"])
        question.set_choice_option(raw_question["choice_options"])
        question.set_classification(raw_question["classification"])
        answers: list[Answer] = [Answer(answer, True) for answer in raw_question["correct_answers"]]
        answers += [Answer(answer, False) for answer in raw_question["wrong_answers"]]
        question.add_answers(answers)
        question.activate()
        questions.add_question(question)
    return questions

def get_config(dir: str) -> Topic:
    filepath: str = path_join(dir, "config.json")
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return Topic(data["title"], data["info"], dir)

def set_config(data: Topic):
    filepath: str = path_join(data.dir, "config.json")
    with open(filepath, "w") as f:
        json.dump({"title": data.title, "info": data.info}, f, indent=4)
        
def get_configs(path: str):
    result: list[Topic] = []
    i: int = 0
    for name in listdir(path):
        full_path = path_join(path, name)
        if isdir(full_path):
            if not exists(path_join(full_path, "config.json")):
                set_config(Topic(f"Sample{i}", "Sample Info", full_path))
            result.append(get_config(full_path))
            i += 1
    return result