class Prompt_Result:
    def __init__(self, **kwargs):
        self.message = ""
        self.value_float = 0
        self.value_string = ""
        self.value_char = ""
        self.value_int = 0
        self.crashed = False
        self.results = []
        self.out_types = []
        self.set_json(**kwargs)
        
    
    def set_json(self, **kwargs):
        for key, value in kwargs.items():
            if key in vars(self).keys():
                setattr(self, key, value)
        return self