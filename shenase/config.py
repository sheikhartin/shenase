import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_URL = os.environ['DATABASE_URL']
TEST_DATABASE_URL = os.environ['TEST_DATABASE_URL']

SESSION_EXPIRE_DAYS = int(os.environ['SESSION_EXPIRE_DAYS'])

AVATAR_UPLOAD_FOLDER = os.environ['AVATAR_UPLOAD_FOLDER']
AVATAR_STORAGE_PATH = os.path.join(BASE_DIR, AVATAR_UPLOAD_FOLDER)
DEFAULT_AVATAR = os.environ['DEFAULT_AVATAR']
