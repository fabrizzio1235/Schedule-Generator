import sqlite3

def init_db():
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    
    # Tabla principal
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            teacher TEXT NOT NULL,
            monday TEXT,
            tuesday TEXT,
            wednesday TEXT,
            thursday TEXT,
            friday TEXT
        )
    ''')

    # Recrear tablas de trabajo asegurando la estructura
    for table in ['scheduleCopy1', 'scheduleCopy2']:
        cursor.execute(f'DROP TABLE IF EXISTS {table}')
        cursor.execute(f'''
            CREATE TABLE {table} (
                id INTEGER PRIMARY KEY,
                subject TEXT,
                teacher TEXT,
                monday TEXT,
                tuesday TEXT,
                wednesday TEXT,
                thursday TEXT,
                friday TEXT
            )
        ''')
    
    conn.commit()
    conn.close()