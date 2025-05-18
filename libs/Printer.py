from os import system as os_system, name as os_name
from time import sleep as delay
    
def print_spacer(amount: int = 1):
    print("\n" * amount, end="")
    
def print_options(data: list[str], start_char = "A"):
    for i in range(len(data)):
        print(f"\t({chr(ord(start_char) + i)}) {data[i]}")
        
def print_question(question: str, number: int):
    print(f"[{number}] {question}")
    
def print_title(text: str, add_separator: bool = False):
    print(f"{["",(10 * "=") + " "][add_separator]}{text.capitalize()}{[""," " + (40 * "=")][add_separator]}")
    

def input_stopper():
    input("Enter any key to continue...")
    
def clear_console():
    delay(0.1)
    os_system('cls' if os_name == 'nt' else 'clear')