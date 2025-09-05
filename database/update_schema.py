import sqlite3, os, bcrypt

def update_schema():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'criminals.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if role column exists
    cursor.execute("PRAGMA table_info(admin)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    
    if 'role' not in column_names:
        print("Adding 'role' column to admin table...")
        cursor.execute("ALTER TABLE admin ADD COLUMN role TEXT DEFAULT 'admin'")
        
        # Update existing admin user to have admin role
        cursor.execute("UPDATE admin SET role = 'admin' WHERE role IS NULL")
        
        # Check if superadmin exists
        cursor.execute("SELECT * FROM admin WHERE username = 'superadmin'")
        superadmin = cursor.fetchone()
        
        if not superadmin:
            print("Creating superadmin user...")
            # Create superadmin user
            super_pw = bcrypt.hashpw(b"superadmin123", bcrypt.gensalt())
            cursor.execute("INSERT INTO admin (username, password, role) VALUES (?, ?, ?)", 
                          ("superadmin", super_pw, "superadmin"))
            print("Superadmin user created with username: superadmin, password: superadmin123")
    else:
        print("Role column already exists in admin table.")
    
    conn.commit()
    conn.close()
    print("Database schema updated successfully.")

if __name__ == '__main__':
    update_schema()