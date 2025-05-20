import firebase_admin
from firebase_admin import credentials, firestore
import json
from os.path import join as path_join, dirname, abspath, isdir
from os import mkdir, pardir

def getdir(filename: str, up_count: int = 0):
    current_dir = dirname(abspath(__file__))
    project_root = abspath(path_join(current_dir, *[pardir for i in range(up_count)]))
    return path_join(project_root, filename)

def upload_topic(TOPIC_NAME: str):
    if not isdir(path_join("data", TOPIC_NAME)):
        print(f"{TOPIC_NAME} does not exists!")
        exit()
    
    # --- INITIALIZE FIREBASE ---
    SERVICE_ACCOUNT_PATH = getdir("service-account.json")
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

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

if __name__ == "__main__":
    upload_topic(input("Topic Name > "))