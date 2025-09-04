import sqlite3

def check_criminals_table():
    conn = sqlite3.connect('database/criminals.db')
    cursor = conn.cursor()
    
    # Get table structure
    cursor.execute('PRAGMA table_info(criminals)')
    print('Criminals table structure:')
    for row in cursor.fetchall():
        print(f"Column: {row[1]}, Type: {row[2]}")
    
    # Get sample data
    cursor.execute('SELECT * FROM criminals LIMIT 3')
    print('\nSample data:')
    for row in cursor.fetchall():
        print(row)
    
    conn.close()

if __name__ == '__main__':
    check_criminals_table()