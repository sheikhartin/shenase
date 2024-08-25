import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_URL = os.environ['DATABASE_URL']
TEST_DATABASE_URL = os.environ['TEST_DATABASE_URL']

JWT_ENCRYPTION_SECRET = os.environ['JWT_ENCRYPTION_SECRET']
JWT_SIGNATURE_METHOD = os.environ['JWT_SIGNATURE_METHOD']
JWT_ACCESS_TOKEN_TTL_MINUTES = int(os.environ['JWT_ACCESS_TOKEN_TTL_MINUTES'])

AVATAR_UPLOAD_FOLDER = os.environ['AVATAR_UPLOAD_FOLDER']
AVATAR_STORAGE_PATH = os.path.join(BASE_DIR, AVATAR_UPLOAD_FOLDER)
DEFAULT_AVATAR = os.environ['DEFAULT_AVATAR']
