from .Prompt_Result import Prompt_Result
from typing import TypeVar
TOptions = TypeVar('TOptions')

def prompt(out_types = ["str", "int", "float", "char"], trials: int = 3, input_text = "> "):
    result = Prompt_Result()
    out_flag = [False for _ in out_types]
    err_counts = 0
    for _ in range(trials):
        temp: str = input(input_text).strip()
        if "str" in out_types:
            result.value_string = temp
            out_flag[out_types.index("str")] = True
            result.out_types.append("str")
        
        if "char" in out_types and len(temp) == 1:
            result.value_char = temp.capitalize()
            out_flag[out_types.index("char")] = True
            result.out_types.append("char")
            
        if any(out in out_types for out in ["float", "int"]):
            try:
                if "float" in out_types:
                    result.value_float = float(temp)
                    out_flag[out_types.index("float")] = True
                    result.out_types.append("float")
                
                if "int" in out_types and (float(temp) == int(temp)):
                    result.value_int = int(temp)
                    out_flag[out_types.index("int")] = True
                    result.out_types.append("int")
            except:
                pass
        
        if not any(out_flag):
            err_counts += 1
            print(f"Give a valid answer!")
            continue
        break
        
    if err_counts == trials:
        result.crashed = True
        
    return result 

def prompt_multiple(repeats: int = 1, out_types = ["str", "int", "float", "char"], trials: int = 3, input_text = "> "):
    results: list[Prompt_Result] = []
    print(f"Prompt {repeats} answers:")
    for _ in range(repeats):
        while True:
            result_temp = prompt(out_types, trials, input_text)
            if result_temp.crashed:
                return result_temp
            out = True
            for result in results:
                if all("str" in each_out_types for each_out_types in [out_types, result_temp.out_types, result.out_types]):
                    out = out and result_temp.value_string != result.value_string
                if all("int" in each_out_types for each_out_types in [out_types, result_temp.out_types, result.out_types]):
                    out = out and result_temp.value_int != result.value_int
                if all("float" in each_out_types for each_out_types in [out_types, result_temp.out_types, result.out_types]):
                    out = out and result_temp.value_float != result.value_float
                if all("char" in each_out_types for each_out_types in [out_types, result_temp.out_types, result.out_types]):
                    out = out and result_temp.value_char != result.value_char
                if not out:
                    break
            if not out:
                print(f"Choose a different answer!")
                continue
            results.append(result_temp)
            break
    return Prompt_Result(results = results)