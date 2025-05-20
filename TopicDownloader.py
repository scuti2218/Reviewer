import firebase_admin
from firebase_admin import credentials, firestore
import json
from os.path import join as path_join, dirname, abspath, isdir
from os import mkdir, pardir, system as os_system, name as os_name
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
    
def get_sub_collection(doc_ref, name: str):
    index_ref = doc_ref.collection(name)
    index_docs = index_ref.stream()
    return [doc.to_dict() for doc in index_docs]
    
def save_json(path: str, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Exported {path}")

# MAINS
def get_all_topics():
    # --- GET ALL DOCUMENTS IN 'Topics' ---
    topics_ref = db.collection("Topics")
    docs = topics_ref.stream()
    
    data = [doc.to_dict() for doc in docs]
    print_title(f"TOPICS {len(data)} FOUND.")
    print_spacer()
    for i, doc in enumerate(data):
        print_title(f"({i}) {doc["title"]}")
        print(f"Topic Key: {doc["token"]}")
        print(f"Title: {doc["title"]}")
        print(f"Version: {doc["version"]}")
        print(f"Information: {doc["info"]}")
        print_divider()
        print_spacer()
    return data

def download_topic(TOPIC_KEY: str):
    # --- GET TOPIC ---
    doc_ref = db.collection("Topics").document(TOPIC_KEY)
    doc = doc_ref.get()
    if not doc.exists:
        print(f"No document found for '{TOPIC_KEY}' in 'Topics'.")
        exit()
    configs_data = doc.to_dict()
    TOPIC_NAME = configs_data["title"]
    
    # --- PATH INITIALIZE ---
    if not isdir("data"):
        mkdir("data")
    PATH_TOPIC = path_join("data", TOPIC_NAME)
    if not isdir(PATH_TOPIC):
        mkdir(PATH_TOPIC)
    PATH_CONFIG = path_join(PATH_TOPIC, "config.json")
    PATH_CATEGORIES = path_join(PATH_TOPIC, "categories.json")
    PATH_INDEX = path_join(PATH_TOPIC, "index.json")

    # --- WRITING TO JSON ---
    save_json(PATH_CONFIG, configs_data)
    save_json(PATH_CATEGORIES, get_sub_collection(doc_ref, "categories"))
    save_json(PATH_INDEX, get_sub_collection(doc_ref, "index"))
    
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
                download_topic(topics[temp_i]["token"])
                print(f"({i}) {topics[temp_i]["title"]} downloaded!")
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