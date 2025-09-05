import sqlite3, os

def update_admin_table():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'criminals.db')
    conn = sqlite3.connect(db_path)
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
    
<<<<<<< HEAD
    # Update existing admin user with sample data
    cursor.execute('''
        UPDATE admin 
        SET first_name = 'Admin', 
            last_name = 'User', 
            email = 'admin@cybersec.local',
            id_number = 'BCD001'
        WHERE username = 'admin' AND (first_name IS NULL OR first_name = '')
    ''')
    
    # Update superadmin user with sample data
    cursor.execute('''
        UPDATE admin 
        SET first_name = 'Super', 
            last_name = 'Admin', 
            email = 'superadmin@cybersec.local',
            id_number = 'BCD000'
        WHERE username = 'superadmin' AND (first_name IS NULL OR first_name = '')
=======
    # Update existing user with sample data
    cursor.execute('''
        UPDATE admin 
        SET first_name = 'Shamsu', 
            last_name = 'Wada', 
            email = 'shawad@biometric.com',
            id_number = 'BCD001'
        WHERE username = 'shawad'
>>>>>>> 667fdcf7b29f05e42dd8ed396f59016ef594fcad
    ''')
    
    conn.commit()
    conn.close()
    print('Admin table schema updated successfully!')

if __name__ == '__main__':
    update_admin_table()