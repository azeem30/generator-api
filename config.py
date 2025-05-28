import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

KEY = os.getenv("KEY")
FERNET = Fernet(KEY.encode()) if KEY else None

# This is the Flask application configuration
APP_CONFIG = {
    "PORT": int(os.getenv("PORT")),
    "HOST": os.getenv("HOST")
}

# This is the MySQL Database Configuration
DB_CONFIG = {
    "HOST": os.getenv("DB_HOST"),
    "PORT": int(os.getenv("DB_PORT")),
    "USER": os.getenv("DB_USER"),
    "PASSWORD": os.getenv("DB_PASSWORD"),
    "DATABASE": os.getenv("DB_NAME")
}

# This is the Mail Service Configuration
MAIL_CONFIG = {
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": 587,
    "SMTP_USERNAME": os.getenv("GMAIL_ADDRESS"),
    "SMTP_PASSWORD": os.getenv("GMAIL_APP_PASSWORD"),
    "EMAIL_FROM": os.getenv("GMAIL_ADDRESS")
}

# This is the model configuration
MODEL_CONFIG = {
    "API_KEY": os.getenv("MODEL_API_KEY"),
    "BASE_URL": os.getenv("MODEL_BASE_URL"),
    "MODEL_NAME": os.getenv("MODEL_NAME")
}
