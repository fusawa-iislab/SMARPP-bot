from db import db
from pydantic import BaseModel, ValidationError
import logging
import time

class Chatlog(BaseModel):
    message: str
    timestamp: str

def create_chatlog(chatlog: dict):
    v = Chatlog(**chatlog)
    doc_ref = db.collection("chatlogs").add(chatlog)
    logging.info(f"Chatlog created with ID: {doc_ref.id}")

# def warm_up_connection():
#     try:
#         logger.info("Firestoreへの接続をウォームアップしています...")
#         start_time = time.time()
#         # 軽い読み取りオペレーションを実行
#         db.collection("chatlogs").limit(1).get()
#         elapsed = time.time() - start_time
#         logger.info(f"接続ウォームアップ完了（{elapsed:.2f}秒）")
#         return True
#     except Exception as e:
#         logger.error(f"接続ウォームアップ失敗: {e}")
        # return False
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    # warm_up_connection()
    # Example usage
    example_chatlog = {
        "message": "Hello, world!",
        "timestamp": "2023-10-01T12:00:00Z"
    }
    
    create_chatlog(example_chatlog)


