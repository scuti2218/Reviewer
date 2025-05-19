from typing import TypeVar, Generic
TData = TypeVar("TData")

class Prompt_Result(Generic[TData]):
    def __init__(self, value: TData, index = -1, **kwargs):
        self.value: TData = value
        self.index = index
        self.message: str = ""
        self.crashed: bool = False
        self.err_val: any = None
        self.configure(**kwargs)

    def configure(self, **kwargs):
        {setattr(self, key, value) for key, value in kwargs.items()}
        return self
    
class Prompt_Results(Prompt_Result[Generic[TData]]):
    def __init__(self, *args: Prompt_Result[TData], **kwargs):
        self.indexes = [prompt_result.index for prompt_result in args]
        self.values = [prompt_result.value for prompt_result in args]
        self.configure(**kwargs)
        super().__init__(value = None, index = -1, **kwargs)