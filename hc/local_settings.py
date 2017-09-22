"""
Setting up database configurations
"""
import os

from dj_database_url import parse

__DBNAME = "postgresql://localhost/hc"
DATABASE_URL = os.getenv('DATABASE_URL') or __DBNAME
SG_KEY = os.environ.get("SG_KEY")

EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_API_KEY = SG_KEY

DATABASES = {
    'default': parse(
        DATABASE_URL,
        conn_max_age=600
    )
}
