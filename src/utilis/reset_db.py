import shutil
import os
from src.config import CHROME_PATH

def reset_database():
    if os.path.exists(CHROME_PATH):
        shutil.rmtree(CHROME_PATH)
        print(f"🗑️ Database at {CHROME_PATH} has been deleted. Ready for a clean start!")
    else:
        print(" No database found to delete.")

if __name__ == "__main__":
    reset_database()