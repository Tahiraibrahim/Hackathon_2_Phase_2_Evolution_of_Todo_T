from sqlmodel import create_engine, text
# Apni database URL yahan paste karein jo .env file mein hai, 
# ya agar .env setup hai to ye code khud utha lega:
from backend.db import engine 

def nuke_tasks_table():
    print("🗑️  Attempting to drop table 'tasks'...")
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS tasks CASCADE;"))
        conn.commit()
    print("✅ Table 'tasks' dropped successfully!")
    print("🔄 Now restart your backend to let it recreate the table correctly.")

if __name__ == "__main__":
    nuke_tasks_table()