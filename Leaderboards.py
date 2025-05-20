import firebase_admin
from firebase_admin import credentials, firestore
import json
from os.path import join as path_join, dirname, abspath, isdir, isfile
from os import mkdir, pardir, system as os_system, name as os_name, listdir
from time import sleep as delay
from datetime import timedelta

# PRINTERS
def clear_console():
    delay(0.1)
    os_system('cls' if os_name == 'nt' else 'clear')
    
count_divider = 60
def print_divider():
    print(count_divider * "=")
    
def print_title(text: str):
    temp_text = text.upper()
    temp = f"== {temp_text} "
    temp += (count_divider - len(temp)) * "="
    print(temp)
    
def print_pause():
    input("Enter any key to continue...")
    
def print_spacer(amount: int = 1):
    print("\n" * amount, end="")

# UTILS
def timedelta_to_words(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())

    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    parts = []
    if days: parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours: parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes: parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds or not parts: parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return ", ".join(parts)

def getdir(filename: str, up_count: int = 0):
    current_dir = dirname(abspath(__file__))
    project_root = abspath(path_join(current_dir, *[pardir for i in range(up_count)]))
    return path_join(project_root, filename)

# MAINS
def get_all_topics():
    if not isdir("data"):
        mkdir("data")
    
    if isdir("data"):
        topics = [dirdata for dirdata in listdir("data") if isfile(path_join("data", dirdata, "config.json"))]
        print_title(f"{len(topics)} TOPICS FOUND.")
        print_spacer()
        data = []
        count = 0
        for i, TOPIC_NAME in enumerate(topics):
            PATH_TOPIC = path_join("data", TOPIC_NAME)
            PATH_CONFIG = path_join(PATH_TOPIC, "config.json")
            with open(PATH_CONFIG, "r", encoding="utf-8") as f:
                doc: dict = json.load(f)
            if str(doc.get("token", "")).strip() != "":
                doc["TOPIC_NAME"] = TOPIC_NAME
                print_title(f"({count}) {doc.get("title")}")
                print(f"Version: {doc.get("version")}")
                print(f"Information: {doc.get("info")}")
                print_divider()
                print_spacer()
                data.append(doc)
                count += 1
    return data

def show_leaderboards(TOPIC_KEY: str, TOPIC_NAME: str):
    clear_console()
    # --- GET ALL DOCUMENTS IN 'Topics' ---
    leaderboards_ref = db.collection("Topics").document(TOPIC_KEY).collection("leaderboards")
    docs = leaderboards_ref.stream()
    
    data = [doc.to_dict() for doc in docs]
    print_title(f"{TOPIC_NAME} ({len(data)} SCORES).")
    for doc in data:
        print(f"Username : {doc["username"]}")
        print(f"Score    : {doc["current"]} / {doc["maximum"]} ({doc["average"]:.2f}%)")
        parts = doc["duration"].split(":")
        h, m, s = map(int, map(float, parts))
        delta = timedelta(hours=h, minutes=m, seconds=s)
        print(f"Duration : {timedelta_to_words(delta)}")
        print(f"{"-" * count_divider}")
    print_divider()
    print_spacer(2)
    
def controller():
    clear_console()
    topics = get_all_topics()
    
    print_title(f"CHOOSE TOPIC")
    print("Choose Topic/s by typing the number/s. Separate them by space.")
    temp = input("> ").split()
    print_spacer()
    for i in temp:
        try:
            temp_i = int(i)
            if temp_i < len(topics):
                show_leaderboards(topics[temp_i]["token"], topics[temp_i]["title"])
            else:
                print(f"({i}) not in list!")
        except ValueError:
            print(f"({i}) is not a number!")

if __name__ == "__main__":
    # --- INITIALIZE FIREBASE ---
    SERVICE_ACCOUNT_PATH = getdir("service-account.json")
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    while True:
        try:
            controller()
            input("Completed! Press enter to reset!")
        except KeyboardInterrupt:
            pass
        
    show_leaderboards(input("Topic Key > "))
    input()