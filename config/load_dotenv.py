from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_PREFIX = os.getenv('API_PREFIX')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS').split(',')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

print(API_PREFIX, DEBUG, ALLOWED_ORIGINS, OPENAI_API_KEY, SECRET_KEY, ALGORITHM)