import firebase_admin
from firebase_admin import credentials, firestore
import json
from os.path import join as path_join, dirname, abspath, isdir
from os import mkdir, pardir

def getdir(filename: str, up_count: int = 0):
    current_dir = dirname(abspath(__file__))
    project_root = abspath(path_join(current_dir, *[pardir for i in range(up_count)]))
    return path_join(project_root, filename)

def download_topic(TOPIC_KEY: str):
    # --- INITIALIZE FIREBASE ---
    SERVICE_ACCOUNT_PATH = getdir("service-account.json")
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

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
    
def get_sub_collection(doc_ref, name: str):
    index_ref = doc_ref.collection(name)
    index_docs = index_ref.stream()
    return [doc.to_dict() for doc in index_docs]
    
def save_json(path: str, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Exported {path}")

if __name__ == "__main__":
    download_topic(input("Topic Key > "))