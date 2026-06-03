from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self.HF_TOKEN = os.getenv("HF_TOKEN")
        self.WEBHOOK_URL = os.getenv("WEBHOOK_URL")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        
config = Config()