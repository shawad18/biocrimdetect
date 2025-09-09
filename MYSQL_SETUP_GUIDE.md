# MySQL Setup Guide
## Converting from SQLite to MySQL

---

## 🎉 **Congratulations!**

You've successfully converted your biometric crime detection system to use MySQL! This guide will help you complete the setup and configuration.

---

## 📋 **Prerequisites**

### **1. MySQL Server Installation**
Ensure you have MySQL Server installed:

**Windows:**
- Download from: https://dev.mysql.com/downloads/mysql/
- Or install via XAMPP: https://www.apachefriends.org/

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

### **2. MySQL Connector for Python**
Install the required Python package:
```bash
pip install mysql-connector-python
```

---

## ⚙️ **Configuration Steps**

### **Step 1: Create MySQL Database**

1. **Login to MySQL:**
```bash
mysql -u root -p
```

2. **Create Database:**
```sql
CREATE DATABASE biometric_crime_detection CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. **Create MySQL User (Recommended):**
```sql
CREATE USER 'biometric_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON biometric_crime_detection.* TO 'biometric_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### **Step 2: Configure Environment Variables**

1. **Copy the example environment file:**
```bash
cp .env.example .env
```

2. **Edit `.env` file with your MySQL credentials:**
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=biometric_crime_detection
MYSQL_USER=biometric_user
MYSQL_PASSWORD=secure_password_here
SECRET_KEY=your-super-secret-key-change-this
```

### **Step 3: Install Updated Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Initialize MySQL Database**
```bash
# Run the MySQL initialization script
python -c "from database.init_mysql import initialize_mysql_database; initialize_mysql_database()"
```

---

## 🚀 **Starting Your Application**

### **Development Mode:**
```bash
# Load environment variables and start
python app.py
```

### **Production Mode:**
```bash
# Set production environment
export FLASK_ENV=production
export DEBUG=False

# Use Gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

---

## 🔧 **What Changed in Your System**

### **New Files Added:**
- `database/mysql_config.py` - MySQL connection management
- `database/init_mysql.py` - MySQL database initialization
- `.env.example` - Environment configuration template
- `MYSQL_SETUP_GUIDE.md` - This setup guide

### **Modified Files:**
- `app.py` - Updated to support both MySQL and SQLite
- `requirements.txt` - Added MySQL connector dependency

### **Enhanced Features:**
- **Connection Pooling** - Better performance with multiple users
- **Environment Configuration** - Secure credential management
- **Automatic Migration** - Your SQLite data is automatically migrated
- **Backward Compatibility** - Falls back to SQLite if MySQL unavailable
- **Enhanced Logging** - Better audit trails and user tracking
- **Production Ready** - Optimized for production deployment

---

## 📊 **Database Schema**

Your MySQL database includes these tables:

### **1. criminals**
- Enhanced with indexes for better performance
- Added timestamps for audit trails
- Support for larger fingerprint/face data

### **2. admin**
- Enhanced user management
- Role-based access control
- Last login tracking
- Email and name fields

### **3. scan_logs** (NEW)
- Comprehensive audit logging
- Scan performance tracking
- User activity monitoring

### **4. system_settings** (NEW)
- Configurable system parameters
- Runtime configuration management

---

## 🔐 **Default Admin Credentials**

After initialization, you can login with:

**Regular Admin:**
- Username: `admin`
- Password: `admin123`

**Super Admin:**
- Username: `superadmin`
- Password: `superadmin123`

⚠️ **IMPORTANT:** Change these passwords immediately in production!

---

## 🛠️ **Using phpMyAdmin**

Now you can use phpMyAdmin to manage your database:

1. **Access phpMyAdmin:** http://localhost/phpmyadmin/
2. **Login** with your MySQL credentials
3. **Select** the `biometric_crime_detection` database
4. **Browse** your tables:
   - `criminals` - Criminal records and biometric data
   - `admin` - System administrators
   - `scan_logs` - Audit logs of all scans
   - `system_settings` - System configuration

### **Useful phpMyAdmin Operations:**

**View Criminal Records:**
```sql
SELECT id, name, crime, date_registered, active 
FROM criminals 
ORDER BY date_registered DESC;
```

**Check Scan Activity:**
```sql
SELECT sl.*, a.username, c.name as criminal_name
FROM scan_logs sl
LEFT JOIN admin a ON sl.admin_id = a.id
LEFT JOIN criminals c ON sl.criminal_id = c.id
ORDER BY scan_timestamp DESC
LIMIT 50;
```

**System Statistics:**
```sql
SELECT 
    COUNT(*) as total_criminals,
    COUNT(CASE WHEN active = 1 THEN 1 END) as active_criminals,
    COUNT(CASE WHEN fingerprint_image IS NOT NULL THEN 1 END) as with_fingerprints,
    COUNT(CASE WHEN face_image IS NOT NULL THEN 1 END) as with_photos
FROM criminals;
```

---

## 🔍 **Troubleshooting**

### **Connection Issues:**

**Error: "Access denied for user"**
```bash
# Check MySQL user permissions
mysql -u root -p
SHOW GRANTS FOR 'biometric_user'@'localhost';
```

**Error: "Can't connect to MySQL server"**
```bash
# Check if MySQL is running
sudo systemctl status mysql  # Linux
brew services list | grep mysql  # macOS
```

**Error: "Database doesn't exist"**
```bash
# Recreate the database
mysql -u root -p
CREATE DATABASE biometric_crime_detection;
```

### **Performance Issues:**

**Slow Queries:**
- Check database indexes
- Monitor connection pool usage
- Review scan_logs table size

**Memory Usage:**
- Adjust MySQL configuration
- Optimize connection pool size
- Consider database cleanup procedures

---

## 📈 **Performance Optimization**

### **MySQL Configuration (my.cnf):**
```ini
[mysqld]
# InnoDB settings for better performance
innodb_buffer_pool_size = 256M
innodb_log_file_size = 64M
innodb_flush_log_at_trx_commit = 2

# Query cache
query_cache_type = 1
query_cache_size = 32M

# Connection settings
max_connections = 100
connect_timeout = 10
```

### **Application Optimization:**
- Use connection pooling (already implemented)
- Implement query result caching
- Regular database maintenance
- Monitor slow query log

---

## 🔄 **Data Migration Verification**

Verify your data was migrated correctly:

```sql
-- Check criminal records count
SELECT COUNT(*) as total_criminals FROM criminals;

-- Check admin users
SELECT username, role, created_at FROM admin;

-- Verify data integrity
SELECT 
    COUNT(*) as total,
    COUNT(CASE WHEN name IS NOT NULL THEN 1 END) as with_names,
    COUNT(CASE WHEN crime IS NOT NULL THEN 1 END) as with_crimes
FROM criminals;
```

---

## 🎯 **Next Steps**

1. **✅ Test Login** - Verify admin login works
2. **✅ Test Scanning** - Try fingerprint/face scanning
3. **✅ Check phpMyAdmin** - Verify database access
4. **✅ Update Passwords** - Change default admin passwords
5. **✅ Configure Backups** - Set up regular database backups
6. **✅ Monitor Performance** - Watch for any performance issues

---

## 📞 **Support**

If you encounter any issues:

1. **Check Logs** - Look at application logs for errors
2. **Verify Configuration** - Double-check .env file settings
3. **Test Connection** - Use MySQL command line to test connectivity
4. **Review Documentation** - Check MySQL and Flask documentation

---

**🎉 Your biometric crime detection system is now running on MySQL with enhanced performance, security, and management capabilities!**