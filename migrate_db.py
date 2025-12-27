"""
Database migration script to add new columns to projects table
Run this once to update your existing database schema
"""

import sqlite3
import os
from pathlib import Path

# Find the database file
db_path = os.path.join(Path(__file__).parent, 'huevault.db')

if not os.path.exists(db_path):
    print(f"Database file not found at {db_path}")
    print("The database will be created automatically when you run the app.")
    exit(0)

print(f"Migrating database at: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get current columns
cursor.execute("PRAGMA table_info(projects)")
columns = [row[1] for row in cursor.fetchall()]

print(f"Current columns: {columns}")

# Define new columns to add
new_columns = {
    'img_width': 'INTEGER DEFAULT 260',
    'img_height': 'INTEGER DEFAULT 200',
    'img_fit': 'VARCHAR(20) DEFAULT "cover"',
    'img_radius': 'INTEGER DEFAULT 8',
    'img_gap': 'INTEGER DEFAULT 16'
}

# Add missing columns
for col_name, col_def in new_columns.items():
    if col_name not in columns:
        print(f"Adding column: {col_name}")
        try:
            cursor.execute(f'ALTER TABLE projects ADD COLUMN {col_name} {col_def}')
            print(f"  [OK] Added {col_name}")
        except Exception as e:
            print(f"  [ERROR] Error adding {col_name}: {e}")
    else:
        print(f"  - Column {col_name} already exists")

conn.commit()
conn.close()

print("\nMigration complete!")
