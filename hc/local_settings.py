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
