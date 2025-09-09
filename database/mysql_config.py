#!/usr/bin/env python3
"""
MySQL Database Configuration and Connection Management
For Biometric Crime Detection System
"""

import mysql.connector
from mysql.connector import Error
import os
from contextlib import contextmanager
import logging

class MySQLConfig:
    """MySQL database configuration and connection management"""
    
    def __init__(self):
        # Database configuration from environment variables or defaults
        self.config = {
            'host': os.environ.get('MYSQL_HOST', 'localhost'),
            'port': int(os.environ.get('MYSQL_PORT', 3306)),
            'database': os.environ.get('MYSQL_DATABASE', 'biometric_crime_detection'),
            'user': os.environ.get('MYSQL_USER', 'root'),
            'password': os.environ.get('MYSQL_PASSWORD', ''),
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': True,
            'raise_on_warnings': True
        }
        
        # Connection pool configuration
        self.pool_config = {
            'pool_name': 'biometric_pool',
            'pool_size': 10,
            'pool_reset_session': True
        }
        
        self.connection_pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize MySQL connection pool"""
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                **self.config,
                **self.pool_config
            )
            print("✅ MySQL connection pool initialized successfully")
        except Error as e:
            print(f"❌ Failed to initialize MySQL connection pool: {e}")
            self.connection_pool = None
    
    @contextmanager
    def get_connection(self):
        """Get a database connection from the pool"""
        connection = None
        try:
            if self.connection_pool:
                connection = self.connection_pool.get_connection()
            else:
                # Fallback to direct connection
                connection = mysql.connector.connect(**self.config)
            
            yield connection
            
        except Error as e:
            if connection:
                connection.rollback()
            print(f"❌ Database error: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a SQL query"""
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params or ())
                
                if fetch:
                    if 'SELECT' in query.upper():
                        if 'LIMIT 1' in query.upper() or query.strip().upper().startswith('SELECT COUNT'):
                            return cursor.fetchone()
                        else:
                            return cursor.fetchall()
                    else:
                        return cursor.fetchone()
                else:
                    connection.commit()
                    return cursor.rowcount
                    
        except Error as e:
            # Handle specific MySQL errors gracefully
            if e.errno == 1050:  # Table already exists
                if 'CREATE TABLE IF NOT EXISTS' in query:
                    print(f"ℹ️ Table already exists, skipping creation")
                    return 0
            elif e.errno == 1007:  # Database already exists
                if 'CREATE DATABASE IF NOT EXISTS' in query:
                    print(f"ℹ️ Database already exists, continuing")
                    return 0
            
            print(f"❌ Query execution error: {e}")
            print(f"Query: {query[:200]}..." if len(query) > 200 else f"Query: {query}")
            print(f"Params: {params}")
            raise
    
    def test_connection(self):
        """Test database connection"""
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result is not None
        except Error as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    def create_database_if_not_exists(self):
        """Create database if it doesn't exist"""
        try:
            # Connect without specifying database
            temp_config = self.config.copy()
            del temp_config['database']
            
            connection = mysql.connector.connect(**temp_config)
            cursor = connection.cursor()
            
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Database '{self.config['database']}' created or already exists")
            
            connection.close()
            
        except Error as e:
            print(f"❌ Failed to create database: {e}")
            raise

# Global MySQL configuration instance
mysql_config = MySQLConfig()

# Convenience functions for backward compatibility
def get_mysql_connection():
    """Get MySQL connection (for backward compatibility)"""
    return mysql_config.get_connection()

def execute_mysql_query(query, params=None, fetch=False):
    """Execute MySQL query (for backward compatibility)"""
    return mysql_config.execute_query(query, params, fetch)

def test_mysql_connection():
    """Test MySQL connection (for backward compatibility)"""
    return mysql_config.test_connection()