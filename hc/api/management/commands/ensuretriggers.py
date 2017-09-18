from django.core.management.base import BaseCommand
from django.db import connection


def _pg(cursor):
    cursor.execute("""
    CREATE OR REPLACE FUNCTION update_alert_after()
    RETURNS trigger AS $update_alert_after$
        BEGIN
            IF NEW.last_ping IS NOT NULL THEN
                NEW.alert_after := NEW.last_ping + NEW.timeout + NEW.grace;
            END IF;
            RETURN NEW;
        END;
    $update_alert_after$ LANGUAGE plpgsql;

    DROP TRIGGER IF EXISTS update_alert_after ON api_check;

    CREATE TRIGGER update_alert_after
    BEFORE INSERT OR UPDATE OF last_ping, timeout, grace  ON api_check
    FOR EACH ROW EXECUTE PROCEDURE update_alert_after();
    """)

    cursor.execute("""
    CREATE OR REPLACE FUNCTION update_alert_before()
    RETURNS trigger AS $update_alert_before$
        BEGIN
            IF NEW.last_ping IS NOT NULL THEN
                NEW.alert_before := NEW.last_ping + NEW.timeout - NEW.grace;
            END IF;
            RETURN NEW;
        END;
    $update_alert_before$ LANGUAGE plpgsql;

    DROP TRIGGER IF EXISTS update_alert_before ON api_check;

    CREATE TRIGGER update_alert_before
    BEFORE INSERT OR UPDATE OF last_ping, timeout, grace ON api_check
    FOR EACH ROW EXECUTE PROCEDURE update_alert_before();
    """)


def _mysql(cursor):
    drop_alert(cursor, "update_alert_after")
    drop_alert(cursor, "update_alert_before")

    cursor.execute("""
    CREATE TRIGGER update_alert_after
    BEFORE UPDATE ON api_check
    FOR EACH ROW SET
        NEW.alert_after =
            NEW.last_ping + INTERVAL (NEW.timeout + NEW.grace) MICROSECOND;
    """)
    cursor.execute("""
    CREATE TRIGGER update_alert_before
    BEFORE UPDATE ON api_check
    FOR EACH ROW SET
        NEW.alert_before =
            NEW.last_ping + INTERVAL (NEW.timeout - NEW.grace) MICROSECOND;
    """)

def _sqlite(cursor):
    drop_alert(cursor, "update_alert_after")
    drop_alert(cursor, "update_alert_before")

    cursor.execute("""
    CREATE TRIGGER update_alert_after
    AFTER UPDATE OF last_ping, timeout, grace ON api_check
    FOR EACH ROW BEGIN
        UPDATE api_check
        SET alert_after =
            datetime(strftime('%s', last_ping) +
            timeout/1000000 + grace/1000000, 'unixepoch')
        WHERE id = OLD.id;
    END;
    """)

    cursor.execute("""
    CREATE TRIGGER update_alert_before
    AFTER UPDATE OF last_ping, timeout, grace ON api_check
    FOR EACH ROW BEGIN
        UPDATE api_check
        SET alert_before =
            datetime(strftime('%s', last_ping) +
            timeout/1000000 - grace/1000000, 'unixepoch')
        WHERE id = OLD.id;
    END;
    """)

def drop_alert(cursor, value):
    """
    Calls the method for dropping a trigger in the database
    """
    cursor.execute("""
    DROP TRIGGER IF EXISTS {};
    """.format(value))



class Command(BaseCommand):
    help = 'Ensures triggers exist in database'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            if connection.vendor == "postgresql":
                _pg(cursor)
                return "Created PostgreSQL trigger"
            if connection.vendor == "mysql":
                _mysql(cursor)
                return "Created MySQL trigger"
            if connection.vendor == "sqlite":
                _sqlite(cursor)
                return "Created SQLite trigger"
