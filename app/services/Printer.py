from os import system as os_system, name as os_name
from time import sleep as delay
    
count_divider = 60
def print_divider():
    print(count_divider * "=")
    
def print_title(text: str, add_separator: bool = False):
    temp_text = text.upper()
    if not add_separator:
        print(temp_text)
        return
    temp = f"== {temp_text} "
    temp += (count_divider - len(temp)) * "="
    print(temp)

def clear_console():
    delay(0.1)
    os_system('cls' if os_name == 'nt' else 'clear')
    
def print_pause():
    input("Enter any key to continue...")
    
def print_spacer(amount: int = 1):
    print("\n" * amount, end="")

def print_question(question: str, num: int = -1):
    print(f"{[f"[{num}]", ""][num == -1]}{question}")
    
def print_options(data: list[str], start_char = "A"):
    for i in range(len(data)):
        print(f"{[start_char, f"({chr(ord(start_char) + i)})"][ord(start_char) in range(65,91)]} {data[i]}")
        
def print_definitions(data: list[str]):
    for i in range(len(data)):
        print(f"- {data[i]}")