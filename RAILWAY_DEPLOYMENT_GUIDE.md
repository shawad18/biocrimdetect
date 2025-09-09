# Railway Deployment Guide

## 🚀 Quick Railway Deployment

Your biometric crime detection system is ready for Railway deployment!

### Prerequisites
- GitHub account
- Railway account (railway.app)
- Your code pushed to GitHub

### Step 1: Prepare Your Repository

```bash
# Ensure all changes are committed
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### Step 2: Deploy to Railway

1. **Go to [railway.app](https://railway.app)**
2. **Sign in with GitHub**
3. **Click "Start a New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your `biometric_crime_detection` repository**
6. **Railway will automatically detect it's a Python Flask app**
7. **Click "Deploy"**

### Step 3: Add MySQL Database

1. **In your Railway project dashboard:**
   - Click **"+ New"**
   - Select **"Database"**
   - Choose **"MySQL"**
   - Wait for database to be created

2. **Get database connection details:**
   - Click on the MySQL service
   - Go to **"Connect"** tab
   - Copy the connection string

### Step 4: Configure Environment Variables

1. **In your Railway project:**
   - Click on your web service
   - Go to **"Variables"** tab
   - Add these variables:

```env
DATABASE_URL=mysql://user:password@host:port/database
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this
PORT=5000
HOST=0.0.0.0
```

### Step 5: Custom Domain (Optional)

1. **In your web service:**
   - Go to **"Settings"** tab
   - Click **"Generate Domain"**
   - Or add your custom domain

### Step 6: Initialize Database

1. **After deployment, visit your app URL**
2. **The app will automatically initialize the MySQL database**
3. **Create admin user using the built-in script**

### Step 7: Test Your Deployment

1. **Visit your Railway app URL**
2. **Test login functionality**
3. **Verify all features work correctly**

## 🔧 Troubleshooting

### Common Issues:

1. **Database Connection Error:**
   - Check DATABASE_URL format
   - Ensure MySQL service is running
   - Verify environment variables

2. **Build Failures:**
   - Check requirements.txt
   - Verify Python version in runtime.txt
   - Check build logs in Railway dashboard

3. **Static Files Not Loading:**
   - Ensure static files are in git repository
   - Check file paths in templates

### Environment Variables Reference:

```env
# Required
DATABASE_URL=mysql://user:pass@host:port/db
SECRET_KEY=your-secret-key

# Optional
FLASK_ENV=production
DEBUG=False
PORT=5000
HOST=0.0.0.0
MAX_CONTENT_LENGTH=16777216
```

## 📊 Monitoring

- **Logs:** Available in Railway dashboard
- **Metrics:** CPU, Memory, Network usage
- **Deployments:** Track deployment history

## 🎯 Post-Deployment

1. **Create admin accounts**
2. **Test all biometric features**
3. **Verify database operations**
4. **Check security settings**
5. **Monitor performance**

## 💰 Pricing

- **Hobby Plan:** $5/month
- **Pro Plan:** $20/month
- **Free tier:** Available for testing

## 🔗 Useful Links

- [Railway Documentation](https://docs.railway.app)
- [Railway Community](https://discord.gg/railway)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)

---

**Your biometric crime detection system is now ready for Railway deployment! 🚀**