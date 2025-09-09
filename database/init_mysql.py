#!/usr/bin/env python3
"""
MySQL Database Initialization Script
Creates tables and initial data for Biometric Crime Detection System
"""

import mysql.connector
from mysql.connector import Error
import bcrypt
import os
from .mysql_config import mysql_config

def create_mysql_tables():
    """Create all necessary tables in MySQL database"""
    
    # Ensure database exists
    try:
        mysql_config.create_database_if_not_exists()
    except Exception as e:
        print(f"⚠️ Database creation check failed, continuing with table creation: {e}")
    
    # Table creation queries
    tables = {
        'criminals': """
            CREATE TABLE IF NOT EXISTS criminals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                crime TEXT,
                case_id VARCHAR(50),
                face_image LONGTEXT,
                fingerprint_image LONGTEXT,
                date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_name (name),
                INDEX idx_case_id (case_id),
                INDEX idx_active (active),
                INDEX idx_date_registered (date_registered)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'admin': """
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password BLOB NOT NULL,
                role ENUM('admin', 'superadmin') DEFAULT 'admin',
                email VARCHAR(255),
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                department VARCHAR(100),
                id_number VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL,
                active BOOLEAN DEFAULT TRUE,
                INDEX idx_username (username),
                INDEX idx_role (role),
                INDEX idx_active (active)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'scan_logs': """
            CREATE TABLE IF NOT EXISTS scan_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                admin_id INT,
                scan_type ENUM('fingerprint', 'face') NOT NULL,
                scan_mode ENUM('single', 'ten_finger', 'live_camera') NOT NULL,
                result_status ENUM('match_found', 'no_match', 'error') NOT NULL,
                criminal_id INT NULL,
                confidence_score DECIMAL(5,2),
                scan_quality DECIMAL(5,2),
                scanner_type VARCHAR(100),
                processing_time DECIMAL(8,3),
                scan_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address VARCHAR(45),
                user_agent TEXT,
                FOREIGN KEY (admin_id) REFERENCES admin(id) ON DELETE SET NULL,
                FOREIGN KEY (criminal_id) REFERENCES criminals(id) ON DELETE SET NULL,
                INDEX idx_scan_timestamp (scan_timestamp),
                INDEX idx_scan_type (scan_type),
                INDEX idx_result_status (result_status),
                INDEX idx_admin_id (admin_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'system_settings': """
            CREATE TABLE IF NOT EXISTS system_settings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                setting_key VARCHAR(100) NOT NULL UNIQUE,
                setting_value TEXT,
                setting_type ENUM('string', 'integer', 'boolean', 'json') DEFAULT 'string',
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_setting_key (setting_key)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    }
    
    try:
        print("🔧 Creating MySQL tables...")
        
        for table_name, create_query in tables.items():
            try:
                mysql_config.execute_query(create_query)
                print(f"✅ Table '{table_name}' created successfully")
            except Error as e:
                print(f"❌ Failed to create table '{table_name}': {e}")
                raise
        
        print("✅ All MySQL tables created successfully")
        
    except Error as e:
        print(f"❌ Failed to create MySQL tables: {e}")
        raise

def create_default_admin_users():
    """Create default admin users"""
    try:
        print("👤 Creating default admin users...")
        
        # Check if admin users already exist
        existing_admins = mysql_config.execute_query(
            "SELECT COUNT(*) as count FROM admin",
            fetch=True
        )
        
        if existing_admins and existing_admins['count'] > 0:
            print("ℹ️ Admin users already exist, skipping creation")
            return
        
        # Create default admin users
        admin_users = [
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
        
        for user in admin_users:
            # Hash password
            hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
            
            # Insert user
            mysql_config.execute_query(
                """
                INSERT INTO admin (username, password, role, email, first_name, last_name)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (user['username'], hashed_password, user['role'], user['email'], user['first_name'], user['last_name'])
            )
            
            print(f"✅ Created admin user: {user['username']} ({user['role']})")
        
        print("✅ Default admin users created successfully")
        
    except Error as e:
        print(f"❌ Failed to create admin users: {e}")
        # Don't raise here, as this is not critical for basic functionality

def create_default_settings():
    """Create default system settings"""
    try:
        print("⚙️ Creating default system settings...")
        
        default_settings = [
            {
                'setting_key': 'fingerprint_match_threshold',
                'setting_value': '75',
                'setting_type': 'integer',
                'description': 'Minimum confidence percentage for fingerprint matches'
            },
            {
                'setting_key': 'face_match_threshold',
                'setting_value': '80',
                'setting_type': 'integer',
                'description': 'Minimum confidence percentage for face matches'
            },
            {
                'setting_key': 'scan_quality_threshold',
                'setting_value': '70',
                'setting_type': 'integer',
                'description': 'Minimum scan quality percentage required'
            },
            {
                'setting_key': 'system_version',
                'setting_value': '3.0.0',
                'setting_type': 'string',
                'description': 'Current system version'
            },
            {
                'setting_key': 'enable_audit_logging',
                'setting_value': 'true',
                'setting_type': 'boolean',
                'description': 'Enable detailed audit logging'
            }
        ]
        
        for setting in default_settings:
            # Check if setting already exists
            existing = mysql_config.execute_query(
                "SELECT id FROM system_settings WHERE setting_key = %s",
                (setting['setting_key'],),
                fetch=True
            )
            
            if not existing:
                mysql_config.execute_query(
                    """
                    INSERT INTO system_settings (setting_key, setting_value, setting_type, description)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (setting['setting_key'], setting['setting_value'], setting['setting_type'], setting['description'])
                )
                print(f"✅ Created setting: {setting['setting_key']}")
        
        print("✅ Default system settings created successfully")
        
    except Error as e:
        print(f"❌ Failed to create system settings: {e}")
        # Don't raise here, as this is not critical

def migrate_sqlite_to_mysql(sqlite_db_path):
    """Migrate data from SQLite to MySQL"""
    try:
        import sqlite3
        
        if not os.path.exists(sqlite_db_path):
            print(f"⚠️ SQLite database not found at {sqlite_db_path}, skipping migration")
            return
        
        print(f"🔄 Migrating data from SQLite to MySQL...")
        
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_db_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Migrate criminals table
        try:
            sqlite_cursor.execute("SELECT * FROM criminals")
            criminals = sqlite_cursor.fetchall()
            
            # Get column names
            sqlite_cursor.execute("PRAGMA table_info(criminals)")
            columns = [column[1] for column in sqlite_cursor.fetchall()]
            
            for criminal in criminals:
                criminal_dict = dict(zip(columns, criminal))
                
                # Check if criminal already exists to prevent duplicates
                existing = mysql_config.execute_query(
                    "SELECT id FROM criminals WHERE name = %s AND crime = %s",
                    (criminal_dict.get('name'), criminal_dict.get('crime')),
                    fetch=True
                )
                
                if not existing:
                    # Insert into MySQL only if not exists
                    mysql_config.execute_query(
                        """
                        INSERT INTO criminals (name, crime, face_image, fingerprint_image)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            criminal_dict.get('name'),
                            criminal_dict.get('crime'),
                            criminal_dict.get('face_image'),
                            criminal_dict.get('fingerprint_image')
                        )
                    )
            
            print(f"✅ Migrated {len(criminals)} criminal records")
            
        except sqlite3.OperationalError as e:
            print(f"⚠️ Could not migrate criminals table: {e}")
        
        # Migrate admin table
        try:
            sqlite_cursor.execute("SELECT * FROM admin")
            admins = sqlite_cursor.fetchall()
            
            # Get column names
            sqlite_cursor.execute("PRAGMA table_info(admin)")
            columns = [column[1] for column in sqlite_cursor.fetchall()]
            
            for admin in admins:
                admin_dict = dict(zip(columns, admin))
                
                # Check if admin already exists
                existing = mysql_config.execute_query(
                    "SELECT id FROM admin WHERE username = %s",
                    (admin_dict.get('username'),),
                    fetch=True
                )
                
                if not existing:
                    mysql_config.execute_query(
                        """
                        INSERT INTO admin (username, password, role)
                        VALUES (%s, %s, %s)
                        """,
                        (
                            admin_dict.get('username'),
                            admin_dict.get('password'),
                            admin_dict.get('role', 'admin')
                        )
                    )
            
            print(f"✅ Migrated {len(admins)} admin records")
            
        except sqlite3.OperationalError as e:
            print(f"⚠️ Could not migrate admin table: {e}")
        
        sqlite_conn.close()
        print("✅ SQLite to MySQL migration completed")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        # Don't raise here, as the system should work without migration

def initialize_mysql_database(sqlite_db_path=None):
    """Complete MySQL database initialization"""
    try:
        print("🚀 Initializing MySQL database for Biometric Crime Detection System")
        print("=" * 70)
        
        # Test connection (this will test with the database name)
        print("🔍 Testing MySQL connection...")
        
        # Try to connect to the specific database first
        try:
            if mysql_config.test_connection():
                print("✅ MySQL connection to database successful")
            else:
                print("⚠️ Cannot connect to specific database, checking if database exists...")
                # Try to create database if connection fails
                if not mysql_config.create_database_if_not_exists():
                    raise Exception("Cannot create or access MySQL database")
        except Exception as conn_error:
            print(f"⚠️ Database connection issue: {conn_error}")
            print("🔧 Attempting to create database...")
            if not mysql_config.create_database_if_not_exists():
                raise Exception("Cannot create or access MySQL database")
        
        # Create tables
        create_mysql_tables()
        
        # Create default admin users
        create_default_admin_users()
        
        # Create default settings
        create_default_settings()
        
        # Migrate from SQLite if path provided
        if sqlite_db_path:
            migrate_sqlite_to_mysql(sqlite_db_path)
        
        print("=" * 70)
        print("🎉 MySQL database initialization completed successfully!")
        print("\n📋 Default Admin Credentials:")
        print("   Username: admin     | Password: admin123")
        print("   Username: superadmin | Password: superadmin123")
        print("\n⚠️  Please change these passwords in production!")
        
        return True
        
    except Exception as e:
        print(f"❌ MySQL database initialization failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Ensure MySQL server is running")
        print("   2. Check your MySQL credentials in .env file")
        print("   3. Verify database permissions")
        print("   4. Try creating the database manually in phpMyAdmin")
        return False

if __name__ == "__main__":
    # Initialize MySQL database
    sqlite_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'criminals.db')
    initialize_mysql_database(sqlite_path)