import sqlite3, os
def create_db():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'criminals.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS criminals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            crime TEXT,
            face_image TEXT,
            fingerprint_image TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password BLOB NOT NULL,
            role TEXT DEFAULT 'admin'
        )
    ''')

    # Insert default admin user username: admin, password: admin123
    import bcrypt
    try:
        # Regular admin
        hashed_pw = bcrypt.hashpw(b"admin123", bcrypt.gensalt())
        cursor.execute("INSERT INTO admin (username, password, role) VALUES (?, ?, ?)", ("admin", hashed_pw, "admin"))
        
        # Superadmin with higher privileges
        super_pw = bcrypt.hashpw(b"superadmin123", bcrypt.gensalt())
        cursor.execute("INSERT INTO admin (username, password, role) VALUES (?, ?, ?)", ("superadmin", super_pw, "superadmin"))
    except Exception as e:
        print(f"[INFO] Admin users already exist or error: {e}")
        pass

    conn.commit()
    conn.close()
    print("[INFO] Database created at", db_path)

if __name__ == '__main__':
    create_db()
