"""
Setting up database configurations
"""
import os

from dj_database_url import parse

__DBNAME = "postgresql://localhost/hc"
DATABASE_URL = os.getenv('DATABASE_URL') or __DBNAME

DATABASES = {
    'default': parse(
        DATABASE_URL,
        conn_max_age=600
    )
}

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
TELEGRAM_AUTH_TOKEN = os.getenv('TELEGRAM_AUTH_TOKEN')
