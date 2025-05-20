from ..views import View
from ..models import Model, Score
from ..services.Printer import print_title, print_question, print_options, print_spacer, print_divider, print_definitions, clear_console, print_pause, delay
from ..services.Prompter import prompt, prompt_multiple
from ..services.Mode import modes, tournament as mode_tournament, quiz as mode_quiz, flashcard as mode_flashback
from ..services import Prompt_Result
from datetime import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self.view = view
        self.model = model
        self.initialize()
        
    def initialize(self):
        self.view.initialize()
        self.model.initialize()
    
    # MAIN MENU ==================================================
    def get_topic(self):
        clear_console()
        self.view.show_header()
        self.model.selected_topic = self.model.topics[0]
        if len(self.model.topics) > 1:
            print_question("Choose your Topic: ", self.config_count)
            topics = [topic.show() for topic in self.model.topics]
            print_spacer()
            print_options(topics)
            print_spacer()
            result_temp = prompt(["char"])
            if (result_temp.crashed):
                self.get_topic()
                return
            result = ord(result_temp.value_char) - 65
            if result not in range(len(topics)):
                print_question(f"Choose only from options A to {chr(65 + len(topics) - 1)}")
                print_pause()
                self.get_topic()
                return
            self.model.selected_topic = self.model.topics[result]
            self.config_count += 1
            print_spacer()
            
        print_divider()
        print_question(f"Topic Selected    : {self.model.selected_topic.title}")
        print_question(f"Topic Information : {self.model.selected_topic.info}")
        print_spacer()
        
        self.model.get_topic_categories()
        categories = [category.show() for category in self.model.categories]
        print_question("Categories: ")
        print_options(categories)
        print_spacer()
        
        self.model.get_topic_questions()
        print_question(f"Total Questions   : {self.model.questions_count}")
        print_divider()
        print_pause()
        
    def get_mode(self):
        clear_console()
        self.view.show_header()
        print_question("Choose your Mode: ", self.config_count)
        print_spacer()
        listed_modes = [(mode.title, mode.listed_info) for mode in modes if mode.active and ((mode.requires_token and self.model.selected_topic.check_token()) or (not mode.requires_token))]
        for i, mode in enumerate(listed_modes):
            print_options([mode[0]], chr(65 + i))
            print_definitions(mode[1])
            print_spacer()
        result_temp = prompt(["char"])
        if (result_temp.crashed):
            self.get_mode()
            return
        result = ord(result_temp.value_char) - 65
        if result not in range(len(listed_modes)):
            print_question(f"Choose only from options A to {chr(65 + len(listed_modes) - 1)}")
            print_pause()
            self.get_mode()
            return
        self.mode = modes[result]
        self.config_count += 1
        print_spacer()
        
        print_divider()
        print_question(f"Mode Selected     : {self.mode.title}")
        print_question(f"Mode Information  : {self.mode.info}")
        for i, info in enumerate(self.mode.listed_info):
            print_question(f"{[" " * 18, "Mode Configuration"][i == 0]} : {info}")
        print_divider()
        print_pause()
        
    def get_amount(self):
        clear_console()
        self.view.show_header()
        questions_count = len(self.model.questions)
        temp_amounts = [10, 30, 60, 100]
        amounts = [i for i in temp_amounts if i < questions_count]
        if len(amounts) != len(temp_amounts):
            amounts.append(questions_count)
            
        self.model.selected_amount = amounts[0]
        if len(amounts) > 1:
            print_question("Choose Amount of Questions: ", self.config_count)
            amounts_txt = [f"{i}" for i in amounts]
            print_spacer()
            print_options(amounts_txt)
            print_spacer()
            result_temp = prompt(["char"])
            if (result_temp.crashed):
                self.get_amount()
                return
            result = ord(result_temp.value_char) - 65
            if result not in range(len(amounts_txt)):
                print_question(f"Choose only from options A to {chr(65 + len(amounts_txt) - 1)}")
                print_pause()
                self.get_amount()
                return
            self.model.selected_amount = amounts[result]
            self.config_count += 1
        else:
            print_question(f"Amount of Questions automatically set to {self.model.selected_amount}")
        print_spacer()
            
        print_divider()
        print_question(f"Amount of Questions : {self.model.selected_amount}")
        print_question(f"Total Questions     : {self.model.questions_count}")
        print_divider()
        print_pause()
        
    def show_configurations(self):
        print_spacer()
        clear_console()
        self.view.show_header()
        print_title(self.model.selected_topic.title, True)
        print_question(f"Information        : {self.model.selected_topic.info}")
        print_question(f"Mode Selected      : {self.mode.title}")
        print_question(f"Mode Information   : {self.mode.info}")
        for i, info in enumerate(self.mode.listed_info):
            print_question(f"{[" " * 18, "Mode Configuration"][i == 0]} : {info}")
        print_question(f"Questions Amount   : {self.model.questions_count}")
        print_divider()
        print_spacer()
        print_pause()
        
    def prompt_restart(self, reask = True):
        print_question("Do you want to restart? ")
        options = ["Yes", "No"]
        print_spacer()
        print_options(options)
        print_spacer()
        
        result_temp = prompt(["char"])
        if (result_temp.crashed):
            if reask:
                return self.prompt_restart()
            return None
        result = ord(result_temp.value_char) - 65
        if result not in range(len(options)):
            print_question(f"Choose only from options A to {chr(65 + len(options) - 1)}")
            print_pause()
            if reask:
                return self.prompt_restart()
            return None
        return result == 0
        
    def prompt_generate_seed(self, reask = True):
        if self.didaskgenerate:
            return False
        self.didaskgenerate = True
        print_question("Generate a seed? ")
        options = ["Yes", "No"]
        print_spacer()
        print_options(options)
        print_spacer()
        
        result_temp = prompt(["char"])
        if (result_temp.crashed):
            if reask:
                return self.prompt_generate_seed()
            return False
        result = ord(result_temp.value_char) - 65
        if result not in range(len(options)):
            print_question(f"Choose only from options A to {chr(65 + len(options) - 1)}")
            print_pause()
            if reask:
                return self.prompt_generate_seed()
            return False
        print_spacer()
        return result == 0
    
    def prompt_submit(self, reask = False):
        if self.didasksubmit:
            return False
        self.didasksubmit = True
        print_question("Submit to leaderboards? ")
        options = ["Yes", "No"]
        print_spacer()
        print_options(options)
        print_spacer()
        
        result_temp = prompt(["char"])
        if (result_temp.crashed):
            if reask:
                return self.prompt_submit()
            return None
        result = ord(result_temp.value_char) - 65
        if result not in range(len(options)):
            print_question(f"Choose only from options A to {chr(65 + len(options) - 1)}")
            print_pause()
            if reask:
                return self.prompt_submit()
            return None
        print_spacer()
        return result == 0
    # MAIN MENU ==================================================
        
        
    # REVIEW ==================================================
    def start(self):
        self.model.score.current = 0
        self.model.score.maximum = 0
        if self.mode.title in [mode_tournament.title, mode_quiz.title]:
            self.model.score.maximum = self.model.selected_amount
        
        self.model.get_randomized_questions()
        questions = self.model.randomized_questions
        i: int = 0
        i_max: int = self.model.selected_amount
        i_max_cur: int = 0
        all_answers: list[list[int]] = [[] for _ in range(i_max)]
        is_corrects: list[bool] = [False for _ in range(i_max)]
        self.temp_score: Score = Score(mode = self.mode.title)
        sent_to_leaderboards = False
        self.didasksubmit = False
        self.didaskgenerate = False
        while i < i_max:
            print_spacer()
            clear_console()
            self.view.show_header()
            
            question = questions[i]
            answers = question.get_randomized_data()
            print_question(question.show(), i+1)
            
            answers_txt = [answer.show() for answer in answers]
            print_spacer()
            print_options(answers_txt)
            print_spacer()
            
            result_temp = prompt_multiple(question.count_correct, ["char", "int"])
            if (result_temp.crashed):
                continue
            results: list[Prompt_Result] = result_temp.results
            
            if any(["int" in each_result.out_types for each_result in results]):
                if not self.mode.back_to_previous:
                    print_question("Going back to previous questions are not allowed!")
                    print_pause()
                    continue
                for each_result in results:
                    if "int" in each_result.out_types:
                        target_i = each_result.value_int - 1
                        if target_i > i_max_cur:
                            print_question("You can only go back to previous questions!")
                            print_pause()
                        elif target_i < -1:
                            print_question("No negative number!")
                            print_pause()
                        else:
                            i = int(each_result.value_int - 1)
                        break
                continue
            
            current_answers = [ord(each_result.value_char) - 65 for each_result in results]
            if not all([ans in range(question.length) for ans in current_answers]):
                print_question(f"Choose only from options A to {chr(65 + question.length - 1)}")
                print_pause()
                continue
            
            all_answers[i] = current_answers
            if self.mode.show_after:
                is_right = all([answers[i].is_correct for i in current_answers])
                self.model.score.maximum += 1
                if is_right:
                    self.model.score.current += 1
                    is_corrects[i] = True
                print_spacer()
                print_title(self.model.get_category(question.category).title, True)
                print_spacer()
                print_question(f"{["❌ Wrong", "✔️ Right"][is_right]} Answer!")
                print_spacer()
                [print_options([answer.title], chr(65 + i)) for i, answer in enumerate(answers) if answer.is_correct]
                print_spacer()
                print_question(self.model.score.show())
                print_divider()
                print_pause()
                if i_max_cur == i:
                    i_max_cur += 1
            i += 1
        self.temp_score.end_datetime = datetime.now()
        self.temp_score.set_duration()
                 
        while True:
            clear_console()
            print_title("Questions", True)
            print_spacer()
            self.model.score.current = 0
            self.model.score.maximum = i_max
            category_scores: dict[str, list[int, int]] = {cat.key : [0, 0] for cat in self.model.categories}
            for i, question in enumerate(questions):
                answers = question.get_randomized_data()
                is_right = all([answers[j].is_correct for j in all_answers[i]])
                if is_right:
                    self.model.score.current += 1
                    is_corrects[i] = True
                    category_scores[question.category][0] += 1
                category_scores[question.category][1] += 1
                
                print_title(f"Question #{i + 1}", True)
                print_question(question.show())
                print_spacer()
                [print_options([answer.title], chr(65 + j)) for j, answer in enumerate(answers)]
                print_spacer()
                
                print_title(f"Your Answer is {["❌ Wrong", "✔️ Right"][is_right]}", True)
                [print_options([answers[j].title], chr(65 + j)) for j in all_answers[i]]
                print_spacer()
                
                print_title("Correct Answers", True)
                [print_options([answer.title], chr(65 + j)) for j, answer in enumerate(answers) if answer.is_correct]
                
                print_divider()
                print_spacer()
                
            print_spacer(3)
            print_title("Final Score", True)
            print_question(self.model.score.show())
            [print_question(f"({key}) {self.model.get_category(key).title} {Score(current = value[0], maximum = value[1]).show()}")  for key, value in category_scores.items() if value[1] != 0]
            print_title("Final Score", True)
            print_spacer(2)
            self.temp_score.current = self.model.score.current
            self.temp_score.maximum = self.model.score.maximum
            self.temp_score.get_average()
            
            onquiz = self.mode.title == mode_quiz.title and self.prompt_submit()
            ontournament = self.mode.title == mode_tournament.title
            leaderboards_const_check = self.model.selected_topic.check_token() and not sent_to_leaderboards
            if self.mode.have_leaderboards and leaderboards_const_check and (onquiz or ontournament):
                print_title("LEADERBOARDS DATA", True)
                self.temp_score.username = input("Username > ")
                print_divider()
                print_spacer()
                self.temp_score.submit(self.model.selected_topic.token)
                sent_to_leaderboards = True
        
            # restart = self.prompt_generate_seed(False)
            # if restart:
            #     # Generate seed
            #     print_title("SEED", True)
            #     seed = "seedsample"
            #     print_question(seed)
            #     print_divider()
            #     print_spacer()
        
            restart = self.prompt_restart(False)
            if restart == None:
                continue
            else:
                return restart
    # REVIEW ==================================================
        
        
    def update(self):
        self.config_count: int = 1
        self.get_topic()
        self.get_mode()
        self.get_amount()
        self.show_configurations()
        
        if self.start():
            self.update()