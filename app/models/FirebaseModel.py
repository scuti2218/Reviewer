import firebase_admin
from firebase_admin import credentials, firestore
from os.path import join as path_join, dirname, abspath
from os import pardir

def getdir(filename: str, up_count: int = 0):
    current_dir = dirname(abspath(__file__))
    project_root = abspath(path_join(current_dir, *[pardir for i in range(up_count)]))
    return path_join(project_root, filename)

SERVICE_ACCOUNT_PATH = getdir("service-account.json", 2)
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()
        
def check_document(TOPIC_KEY: str):
    return db.collection("Topics").document(TOPIC_KEY).get().exists

def set_leaderboards_data(TOPIC_KEY: str, SCORE_KEY, data):
    leaderboard_ref = db.collection("Topics").document(TOPIC_KEY).collection("leaderboards").document(SCORE_KEY)
    leaderboard_ref.set(data)