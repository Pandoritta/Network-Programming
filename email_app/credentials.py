import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv('EMAIL')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRETS_FILE = os.path.abspath(os.path.join(BASE_DIR, '../../..', 'client_secret.json'))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'email_downloads')
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'token.json')
SCOPES = ['https://mail.google.com/']
REDIRECT_URI = 'https://localhost:8080' 
