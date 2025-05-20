import firebase_admin
from firebase_admin import credentials, firestore
from os.path import join as path_join, dirname, abspath
from os import pardir

def getdir(filename: str, up_count: int = 0):
    current_dir = dirname(abspath(__file__))
    project_root = abspath(path_join(current_dir, *[pardir for i in range(up_count)]))
    return path_join(project_root, filename)

def get_all_topics():
    # --- INITIALIZE FIREBASE ---
    SERVICE_ACCOUNT_PATH = getdir("service-account.json")
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # --- GET ALL DOCUMENTS IN 'Topics' ---
    topics_ref = db.collection("Topics")
    docs = topics_ref.stream()
    
    data = [doc.to_dict() for doc in docs]
    print(f"TOPICS {len(data)} FOUND.")
    print(f"{"-" * 40}\n")
    for doc in data:
        print(f"Topic Key: {doc["token"]}")
        print(f"Title: {doc["title"]}")
        print(f"Version: {doc["version"]}")
        print(f"Information: {doc["info"]}")
        print(f"{"-" * 40}\n")

if __name__ == "__main__":
    get_all_topics()
    input()