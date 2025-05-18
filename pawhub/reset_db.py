import os
import django
import mysql.connector
from django.core.management import call_command

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawhub.settings')
django.setup()

def reset_database():
    # Connect to MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='divya'
    )
    cursor = conn.cursor()
    
    # Drop and recreate database
    cursor.execute("DROP DATABASE IF EXISTS pawhub_db")
    cursor.execute("CREATE DATABASE pawhub_db")
    
    cursor.close()
    conn.close()

def apply_migrations():
    # Apply migrations in correct order
    migrations = [
        'auth',
        'contenttypes',
        'admin',
        'sessions',
        'users',
        'pets',
        'core',
        'lost_found',
        'hospitals'
    ]
    
    for app in migrations:
        print(f"Applying migrations for {app}...")
        call_command('migrate', app)

if __name__ == '__main__':
    print("Resetting database...")
    reset_database()
    print("Applying migrations...")
    apply_migrations()
    print("Done!") 