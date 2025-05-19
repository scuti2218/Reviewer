from ..services.CRUD import check_dir, make_dir, get_configs, get_categories, get_questions
from ..services import Randomizable
from .Topic import Topic
from .Category import Category
from .Question import Question
from .Score import Score

class Model:
    def __init__(self):
        self.topics: list[Topic] = []
        self.categories: list[Topic] = []
        self.selected_topic: Topic = None
        self.selected_amount: int = 0
        self.randomizer = Randomizable[Question]()
        self.randomized_questions = []
        self.score: Score = Score()
    
    def initialize(self):
        self.init_topics()
    
    def init_topics(self):
        if not check_dir("data"):
            make_dir("data")
            
        topics = get_configs("data")
        if len(topics) == 0:
            input("Add Topics in Data!")
            return False
        self.topics = topics
        return True
    
    def get_topic_categories(self):
        self.categories: list[Category] = get_categories(self.selected_topic.dir)
        return len(self.categories) != 0
    
    def get_topic_questions(self):
        self.questions: list[Question] = get_questions(self.selected_topic.dir)
        self.questions_count = len(self.questions)
        self.randomizer.set_value(*self.questions)
        return len(self.questions) != 0
    
    def get_randomized_questions(self):
        self.randomized_questions = self.randomizer.randomize()[:self.selected_amount]
        [question.randomize() for question in self.randomized_questions]
        
    def get_category(self, key: str):
        for category in self.categories:
            if category.key == key:
                return category
        return None