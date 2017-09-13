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

TWILIO_ACCOUNT_SID = "AC0d68879d3fea1077ca56886824416583"
TWILIO_AUTH_TOKEN = "cec0e6c3559978227e4c2f3cd63a20db"
TWILIO_NUMBER = "+13345170889"
