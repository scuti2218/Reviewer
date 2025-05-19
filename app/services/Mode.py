from ..models import ModelData

class Mode(ModelData):
    modes: list = []
    def __init__(self, title: str, info: str, listed_info: str, **kwargs):
        self.active = True
        self.listed_info = listed_info
        self.modes.append(self)
        
        self.requires_token = True
        self.show_after: bool = True # True: after question, False: on end
        self.have_leaderboards: bool = True
        self.back_to_previous: bool = True # Ability to go back to previous questions
        
        super().__init__(title = title, info = info, **kwargs)
        
    def show(self):
        return f"{self.title} : {self.info}"
        
tournament = Mode("Tournament",
                  "Tournament Mode",
                  ["Show results at the end",
                   "Have leaderboards",
                   "Cannot go back to previous questions"],
                  requires_token = True,
                  show_after = False,
                  have_leaderboards = True,
                  back_to_previous = False)
quiz = Mode("Quiz",
            "Quiz Mode",
            ["Show results at the end",
             "Have leaderboards",
             "Can go back to previous question"],
                  requires_token = False,
                  show_after = False,
                  have_leaderboards = True,
                  back_to_previous = True)
flashcard = Mode("Flashcard",
                 "Flashcard Mode",
                 ["Show results after each questions",
                  "No leaderboards",
                  "Cannot go back to previous questions"],
                  requires_token = False,
                  show_after = True,
                  have_leaderboards = False,
                  back_to_previous = False)
custom = Mode("Custom",
              "Custom Mode",
              ["Configurations vary"],
              active = False)
        
modes = [tournament, quiz, flashcard, custom]