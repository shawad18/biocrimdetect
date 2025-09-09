#!/usr/bin/env python3
"""
Create New Admin User Script
Creates fresh admin credentials for easy access
"""

import os
import sys
import bcrypt

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database.mysql_config import mysql_config
    MYSQL_AVAILABLE = True
    print("✅ MySQL configuration loaded")
except ImportError:
    MYSQL_AVAILABLE = False
    import sqlite3
    print("⚠️ MySQL not available, using SQLite")

def create_new_admin():
    """
    Create new admin user with simple credentials
    """
    print("🔐 Creating New Admin User")
    print("=" * 40)
    
    # Simple, easy-to-remember credentials
    new_admin = {
        'username': 'admin',
        'password': 'password123',
        'role': 'superadmin',
        'email': 'admin@system.local',
        'first_name': 'System',
        'last_name': 'Administrator'
    }
    
    if MYSQL_AVAILABLE:
        # MySQL admin creation
        print("📊 Creating MySQL admin user...")
        
        # Hash the password
        hashed_password = bcrypt.hashpw(new_admin['password'].encode('utf-8'), bcrypt.gensalt())
        
        # Delete existing admin user if exists
        mysql_config.execute_query(
            "DELETE FROM admin WHERE username = %s",
            (new_admin['username'],)
        )
        print(f"🗑️ Removed existing user: {new_admin['username']}")
        
        # Insert new admin user
        mysql_config.execute_query(
            """
            INSERT INTO admin (username, password, role, email, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (new_admin['username'], hashed_password, new_admin['role'], 
             new_admin['email'], new_admin['first_name'], new_admin['last_name'])
        )
        print(f"✅ Created new admin user: {new_admin['username']}")
        
        # Verify creation
        result = mysql_config.execute_query(
            "SELECT username, role, email FROM admin WHERE username = %s",
            (new_admin['username'],),
            fetch=True
        )
        
        if result:
            print(f"✅ Verification successful: {result}")
        else:
            print("❌ Verification failed")
        
    else:
        # SQLite admin creation
        print("📊 Creating SQLite admin user...")
        
        db_path = os.path.join(os.path.dirname(__file__), 'criminals.db')
        if not os.path.exists(db_path):
            print(f"⚠️ SQLite database not found at {db_path}")
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Hash the password
        hashed_password = bcrypt.hashpw(new_admin['password'].encode('utf-8'), bcrypt.gensalt())
        
        # Delete existing admin user if exists
        cursor.execute("DELETE FROM admin WHERE username = ?", (new_admin['username'],))
        print(f"🗑️ Removed existing user: {new_admin['username']}")
        
        # Insert new admin user
        cursor.execute(
            "INSERT INTO admin (username, password, role) VALUES (?, ?, ?)",
            (new_admin['username'], hashed_password, new_admin['role'])
        )
        print(f"✅ Created new admin user: {new_admin['username']}")
        
        conn.commit()
        conn.close()
    
    return new_admin

def main():
    """
    Main function to create new admin
    """
    try:
        # Create new admin
        admin = create_new_admin()
        
        print("\n🎉 New Admin User Created Successfully!")
        print("\n📋 Login Credentials:")
        print(f"   👤 Username: {admin['username']}")
        print(f"   🔑 Password: {admin['password']}")
        print(f"   🛡️ Role: {admin['role']}")
        print("\n🌐 Login URL: http://127.0.0.1:5002/login")
        print("\n💡 These are simple credentials for easy access!")
        print("⚠️ Change the password after first login for security.")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())