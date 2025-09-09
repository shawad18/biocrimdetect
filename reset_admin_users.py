#!/usr/bin/env python3
"""
Reset Admin Users Script
Deletes all existing admin users and creates new ones with specified credentials
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

def reset_admin_users():
    """
    Delete all existing admin users and create new ones
    """
    print("🔄 Resetting admin users...")
    
    if MYSQL_AVAILABLE:
        # MySQL admin reset
        print("📊 Resetting MySQL admin users...")
        
        # First, delete all existing admin users
        mysql_config.execute_query("DELETE FROM admin")
        print("🗑️ Deleted all existing admin users")
        
        # Create new admin users
        new_admin_users = [
            {
                'username': 'shawad',
                'password': 'Sunee@18',
                'role': 'admin',
                'email': 'shawad@biometric-system.local',
                'first_name': 'Shawad',
                'last_name': 'Administrator'
            },
            {
                'username': 'SHAMSU',
                'password': '#Sunainah@18',
                'role': 'superadmin',
                'email': 'shamsu@biometric-system.local',
                'first_name': 'Shamsu',
                'last_name': 'Super Administrator'
            }
        ]
        
        for user in new_admin_users:
            # Hash the password
            hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
            
            # Insert new user
            mysql_config.execute_query(
                """
                INSERT INTO admin (username, password, role, email, first_name, last_name)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (user['username'], hashed_password, user['role'], 
                 user['email'], user['first_name'], user['last_name'])
            )
            print(f"✅ Created user: {user['username']} ({user['role']})")
        
        print("✅ MySQL admin users reset successfully")
        
    else:
        # SQLite admin reset
        print("📊 Resetting SQLite admin users...")
        
        db_path = os.path.join(os.path.dirname(__file__), 'criminals.db')
        if not os.path.exists(db_path):
            print(f"⚠️ SQLite database not found at {db_path}")
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Delete all existing admin users
        cursor.execute("DELETE FROM admin")
        print("🗑️ Deleted all existing admin users")
        
        # Create new admin users
        new_admin_users = [
            {
                'username': 'shawad',
                'password': 'Sunee@18',
                'role': 'admin'
            },
            {
                'username': 'SHAMSU',
                'password': '#Sunainah@18',
                'role': 'superadmin'
            }
        ]
        
        for user in new_admin_users:
            # Hash the password
            hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
            
            # Insert new user
            cursor.execute(
                "INSERT INTO admin (username, password, role) VALUES (?, ?, ?)",
                (user['username'], hashed_password, user['role'])
            )
            print(f"✅ Created user: {user['username']} ({user['role']})")
        
        conn.commit()
        conn.close()
        
        print("✅ SQLite admin users reset successfully")

def verify_new_users():
    """
    Verify that the new users were created successfully
    """
    print("\n🔍 Verifying new admin users...")
    
    if MYSQL_AVAILABLE:
        # Check MySQL users
        users = mysql_config.execute_query(
            "SELECT username, role, email, first_name, last_name FROM admin ORDER BY role",
            fetch=True
        )
        
        if users:
            print("📋 Current admin users in MySQL:")
            for user in users:
                print(f"   👤 {user['username']} ({user['role']}) - {user['first_name']} {user['last_name']}")
                print(f"      📧 {user['email']}")
        else:
            print("⚠️ No admin users found in MySQL")
        
    else:
        # Check SQLite users
        db_path = os.path.join(os.path.dirname(__file__), 'criminals.db')
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT username, role FROM admin ORDER BY role")
            users = cursor.fetchall()
            
            if users:
                print("📋 Current admin users in SQLite:")
                for user in users:
                    print(f"   👤 {user[0]} ({user[1]})")
            else:
                print("⚠️ No admin users found in SQLite")
            
            conn.close()

def main():
    """
    Main function to reset admin users
    """
    print("🔐 Admin Users Reset Tool")
    print("=" * 40)
    
    try:
        # Reset admin users
        reset_admin_users()
        
        # Verify new users
        verify_new_users()
        
        print("\n🎉 Admin users reset successfully!")
        print("\n📋 New Login Credentials:")
        print("   👤 Admin: shawad / Sunee@18")
        print("   👤 Superadmin: SHAMSU / #Sunainah@18")
        print("\n💡 You can now login with these new credentials")
        print("🌐 Local URL: http://127.0.0.1:5001/login")
        
    except Exception as e:
        print(f"❌ Error during admin reset: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())