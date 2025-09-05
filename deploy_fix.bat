@echo off
echo ========================================
echo   CSRF Fix Deployment Script
echo ========================================
echo.
echo This script will:
echo 1. Add changes to git
echo 2. Commit the CSRF fix
echo 3. Push to GitHub
echo.
pause
echo.
echo Adding changes to git...
git add .
echo.
echo Committing CSRF fix...
git commit -m "Fix CSRF configuration for Heroku production deployment"
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Go to your Heroku dashboard
echo 2. Click "Deploy" tab
echo 3. Click "Deploy Branch" to redeploy
echo 4. Test your app at: https://bmds-35cc80c0e5ba.herokuapp.com/login
echo.
pause