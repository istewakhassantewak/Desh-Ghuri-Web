import sqlite3

# Path to your SQLite database file
DB_PATH = 'db.sqlite3'

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Delete the migration record for the faulty migration
cursor.execute("DELETE FROM django_migrations WHERE app='auth_app' AND name='0002_add_reset_token'")
conn.commit()

# Check if the row was deleted
cursor.execute("SELECT * FROM django_migrations WHERE app='auth_app' AND name='0002_add_reset_token'")
rows = cursor.fetchall()
if not rows:
    print('Migration record deleted successfully.')
else:
    print('Migration record still exists.')

conn.close()
