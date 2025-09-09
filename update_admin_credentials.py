#!/usr/bin/env python3
"""
Update Admin Credentials Script
Updates existing admin users with new credentials
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

def update_admin_credentials():
    """
    Update existing admin credentials with new ones
    """
    print("🔄 Updating admin credentials...")
    
    if MYSQL_AVAILABLE:
        # MySQL credential update
        print("📊 Updating MySQL admin credentials...")
        
        # New admin users
        new_admin_users = [
            {
                'old_username': 'admin',
                'new_username': 'shawad',
                'password': 'Sunee@18',
                'role': 'admin',
                'email': 'shawad@biometric-system.local',
                'first_name': 'Shawad',
                'last_name': 'Administrator'
            },
            {
                'old_username': 'superadmin',
                'new_username': 'SHAMSU',
                'password': '#Sunainah@18',
                'role': 'superadmin',
                'email': 'shamsu@biometric-system.local',
                'first_name': 'Shamsu',
                'last_name': 'Super Administrator'
            }
        ]
        
        for user in new_admin_users:
            # Hash the new password
            hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
            
            # Check if old user exists
            existing = mysql_config.execute_query(
                "SELECT id FROM admin WHERE username = %s",
                (user['old_username'],),
                fetch=True
            )
            
            if existing:
                # Update existing user
                mysql_config.execute_query(
                    """
                    UPDATE admin 
                    SET username = %s, password = %s, email = %s, first_name = %s, last_name = %s
                    WHERE username = %s
                    """,
                    (user['new_username'], hashed_password, user['email'], 
                     user['first_name'], user['last_name'], user['old_username'])
                )
                print(f"✅ Updated user: {user['old_username']} → {user['new_username']}")
            else:
                # Create new user if old one doesn't exist
                mysql_config.execute_query(
                    """
                    INSERT INTO admin (username, password, role, email, first_name, last_name)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (user['new_username'], hashed_password, user['role'], 
                     user['email'], user['first_name'], user['last_name'])
                )
                print(f"✅ Created new user: {user['new_username']}")
        
        print("✅ MySQL admin credentials updated successfully")
        
    else:
        # SQLite credential update
        print("📊 Updating SQLite admin credentials...")
        
        db_path = os.path.join(os.path.dirname(__file__), 'criminals.db')
        if not os.path.exists(db_path):
            print(f"⚠️ SQLite database not found at {db_path}")
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # New admin users for SQLite
        new_admin_users = [
            {
                'old_username': 'admin',
                'new_username': 'shawad',
                'password': 'Sunee@18',
                'role': 'admin'
            },
            {
                'old_username': 'superadmin',
                'new_username': 'SHAMSU',
                'password': '#Sunainah@18',
                'role': 'superadmin'
            }
        ]
        
        for user in new_admin_users:
            # Hash the new password
            hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
            
            # Check if old user exists
            cursor.execute("SELECT id FROM admin WHERE username = ?", (user['old_username'],))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing user
                cursor.execute(
                    "UPDATE admin SET username = ?, password = ? WHERE username = ?",
                    (user['new_username'], hashed_password, user['old_username'])
                )
                print(f"✅ Updated user: {user['old_username']} → {user['new_username']}")
            else:
                # Create new user if old one doesn't exist
                cursor.execute(
                    "INSERT INTO admin (username, password, role) VALUES (?, ?, ?)",
                    (user['new_username'], hashed_password, user['role'])
                )
                print(f"✅ Created new user: {user['new_username']}")
        
        conn.commit()
        conn.close()
        
        print("✅ SQLite admin credentials updated successfully")

def verify_credentials():
    """
    Verify that the new credentials work
    """
    print("\n🔍 Verifying new credentials...")
    
    if MYSQL_AVAILABLE:
        # Check MySQL credentials
        users = mysql_config.execute_query(
            "SELECT username, role, email, first_name, last_name FROM admin ORDER BY role",
            fetch=True
        )
        
        if users:
            print("📋 Current admin users in MySQL:")
            for user in users:
                print(f"   👤 {user['username']} ({user['role']}) - {user['first_name']} {user['last_name']}")
        else:
            print("⚠️ No admin users found in MySQL")
        
    else:
        # Check SQLite credentials
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
    Main function to update admin credentials
    """
    print("🔐 Admin Credentials Update Tool")
    print("=" * 40)
    
    try:
        # Update credentials
        update_admin_credentials()
        
        # Verify credentials
        verify_credentials()
        
        print("\n🎉 Admin credentials updated successfully!")
        print("\n📋 New Login Credentials:")
        print("   👤 Admin: shawad / Sunee@18")
        print("   👤 Superadmin: SHAMSU / #Sunainah@18")
        print("\n💡 Restart your Flask application to use the new credentials")
        
    except Exception as e:
        print(f"❌ Error during credential update: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())