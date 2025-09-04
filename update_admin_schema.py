import sqlite3

def update_admin_table():
    conn = sqlite3.connect('database/criminals.db')
    cursor = conn.cursor()
    
    # Add new columns to admin table
    columns_to_add = [
        ('first_name', 'TEXT'),
        ('last_name', 'TEXT'),
        ('email', 'TEXT'),
        ('id_number', 'TEXT')
    ]
    
    for column_name, column_type in columns_to_add:
        try:
            cursor.execute(f'ALTER TABLE admin ADD COLUMN {column_name} {column_type}')
            print(f'Added column: {column_name}')
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e):
                print(f'Column {column_name} already exists')
            else:
                print(f'Error adding column {column_name}: {e}')
    
    # Update existing user with sample data
    cursor.execute('''
        UPDATE admin 
        SET first_name = 'Shamsu', 
            last_name = 'Wada', 
            email = 'shawad@biometric.com',
            id_number = 'BCD001'
        WHERE username = 'shawad'
    ''')
    
    conn.commit()
    conn.close()
    print('Admin table schema updated successfully!')

if __name__ == '__main__':
    update_admin_table()