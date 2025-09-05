import sqlite3, os
import random

def update_criminals_table():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'criminals.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add new columns to criminals table
    columns_to_add = [
        ('age', 'INTEGER'),
        ('case_id', 'TEXT'),
        ('first_name', 'TEXT'),
        ('last_name', 'TEXT'),
        ('suspect_photo', 'TEXT'),
        ('date_of_birth', 'DATE')
    ]
    
    for column_name, column_type in columns_to_add:
        try:
            cursor.execute(f'ALTER TABLE criminals ADD COLUMN {column_name} {column_type}')
            print(f'Added column: {column_name}')
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e):
                print(f'Column {column_name} already exists')
            else:
                print(f'Error adding column {column_name}: {e}')
    
    # Add sample data if table is empty
    cursor.execute('SELECT COUNT(*) FROM criminals')
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_criminals = [
            ('John', 'Doe', 28, 'CC-45321', 'Phishing & Identity Theft', 'john_doe.jpg', 'john_doe_fp.jpg'),
            ('Sarah', 'Wilson', 34, 'CC-78945', 'Credit Card Fraud', 'sarah_wilson.jpg', 'sarah_wilson_fp.jpg'),
            ('Mike', 'Johnson', 42, 'CC-12367', 'Money Laundering', 'mike_johnson.jpg', 'mike_johnson_fp.jpg'),
            ('Lisa', 'Brown', 29, 'CC-89012', 'Cyberstalking', 'lisa_brown.jpg', 'lisa_brown_fp.jpg')
        ]
        
        for criminal in sample_criminals:
            cursor.execute('''
                INSERT INTO criminals (first_name, last_name, age, case_id, crime, face_image, fingerprint_image, name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (*criminal, f"{criminal[0]} {criminal[1]}"))
        
        print(f'Added {len(sample_criminals)} sample criminals')
    else:
        print(f'Table already has {count} records')
    
    conn.commit()
    conn.close()
    print('Criminals table schema updated successfully!')

if __name__ == '__main__':
    update_criminals_table()