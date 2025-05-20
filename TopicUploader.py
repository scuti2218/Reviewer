import firebase_admin
from firebase_admin import credentials, firestore
import json
from os.path import join as path_join, dirname, abspath, isdir, isfile
from os import mkdir, pardir, system as os_system, name as os_name, listdir
from time import sleep as delay

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
        print_title(f"TOPICS {len(topics)} FOUND.")
        data = []
        for i, TOPIC_NAME in enumerate(topics):
            PATH_TOPIC = path_join("data", TOPIC_NAME)
            PATH_CONFIG = path_join(PATH_TOPIC, "config.json")
            with open(PATH_CONFIG, "r", encoding="utf-8") as f:
                doc: dict = json.load(f)
            data.append(doc)
            doc["TOPIC_NAME"] = TOPIC_NAME
            print_title(f"({i}) {doc.get("title")}")
            print(f"Version: {doc.get("version")}")
            print(f"Information: {doc.get("info")}")
            print_divider()
            print_spacer()
    return data

def upload_topic(TOPIC_NAME: str):
    # --- PATH INITIALIZE ---
    PATH_TOPIC = path_join("data", TOPIC_NAME)
    PATH_CONFIG = path_join(PATH_TOPIC, "config.json")
    PATH_CATEGORIES = path_join(PATH_TOPIC, "categories.json")
    PATH_INDEX = path_join(PATH_TOPIC, "index.json")
    with open(PATH_CONFIG, 'r', encoding='utf-8') as file:
        data = json.load(file)
    TOPIC_KEY = data["token"]

    # --- UPLOAD MAIN DOCUMENT CONFIG (configs.json) ---
    with open(PATH_CONFIG, "r") as f:
        config_data = json.load(f)
    doc_ref = db.collection("Topics").document(TOPIC_KEY)
    doc_ref.set(config_data)
    print(f"Uploaded configs.json to Topics/{TOPIC_NAME}")

    # --- UPLOAD categories.json ---
    with open(PATH_CATEGORIES, "r") as f:
        categories_data = json.load(f)
    categories_ref = doc_ref.collection("categories")
    for doc_fields in categories_data:
        categories_ref.document(doc_fields["token"]).set(doc_fields)
    print(f"Uploaded categories.json to Topics/{TOPIC_NAME}/categories")

    # --- UPLOAD index.json ---
    with open(PATH_INDEX, "r") as f:
        index_data: list[dict] = json.load(f)
    index_ref = doc_ref.collection("index")
    for doc_fields in index_data:
        index_ref.document(doc_fields["token"]).set(doc_fields)
    print(f"Uploaded index.json to Topics/{TOPIC_NAME}/index")
    
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
                upload_topic(topics[temp_i]["TOPIC_NAME"])
                print(f"({i}) {topics[temp_i]["title"]} uploaded!")
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