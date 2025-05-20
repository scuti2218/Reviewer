from .ModelData import ModelData
from datetime import datetime
import hashlib
from .FirebaseModel import set_leaderboards_data

class Score(ModelData):
    def __init__(self, **kwargs):
        self.username: str = ""
        self.current: int = 0
        self.maximum: int = 0
        self.datetime: datetime = datetime.now()
        self.duration: datetime = datetime.now()
        self.start_datetime: datetime = datetime.now()
        self.end_datetime: datetime = datetime.now()
        self.mode: str = ""
        super().__init__(**kwargs)
        self.info = f"Score of {self.title}"
        if self.maximum != 0:
            self.get_average()
    
    def show(self):
        return f"{self.current} / {self.maximum} ({self.get_average():.2f} %)"
    
    def get_average(self):
        self.average = (self.current * 100) / self.maximum
        return self.average
    
    def check_token(self):
        return True
    
    def set_duration(self):
        self.duration = self.end_datetime - self.start_datetime
        
    def set_key(self):
        data = ":".join([self.username, self.attrchange("datetime")])
        self.title = hashlib.sha256(data.encode()).hexdigest()
        self.info = f"Score of {self.username}"
        return self.title
    
    def submit(self, topic_key: str):
        if self.check_token():
            set_leaderboards_data(topic_key, self.set_key(), self.get_json())
            
    def get_json(self):
        data = super().get_json()
        data["datetime"] = self.attrchange("datetime")
        data["start_datetime"] = self.attrchange("start_datetime")
        data["end_datetime"] = self.attrchange("end_datetime")
        data["duration"] = str(self.duration)
        return data
    
    def attrchange(self, name):
        data: datetime = getattr(self, name)
        return data.strftime("%Y-%m-%d %H:%M:%S")
        