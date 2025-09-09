#!/usr/bin/env python3
"""
Railway Deployment Helper Script
This script helps prepare and deploy the biometric crime detection system to Railway.
"""

import os
import subprocess
import sys

def check_git_status():
    """Check if there are uncommitted changes"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("⚠️  Warning: You have uncommitted changes:")
            print(result.stdout)
            return False
        return True
    except subprocess.CalledProcessError:
        print("❌ Error: Not a git repository or git not installed")
        return False

def update_requirements():
    """Update requirements.txt with current environment"""
    try:
        print("📦 Updating requirements.txt...")
        subprocess.run([sys.executable, '-m', 'pip', 'freeze'], 
                      stdout=open('requirements.txt', 'w'), check=True)
        print("✅ Requirements updated successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error updating requirements.txt")
        return False

def commit_changes():
    """Commit all changes for deployment"""
    try:
        print("📝 Committing changes...")
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Prepare for Railway deployment'], check=True)
        print("✅ Changes committed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error committing changes")
        return False

def push_to_github():
    """Push changes to GitHub"""
    try:
        print("🚀 Pushing to GitHub...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("✅ Pushed to GitHub successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error pushing to GitHub")
        return False

def main():
    """Main deployment preparation function"""
    print("🚂 Railway Deployment Helper")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Run this script from the project root.")
        sys.exit(1)
    
    # Update requirements
    if not update_requirements():
        sys.exit(1)
    
    # Check git status
    if not check_git_status():
        response = input("\nDo you want to commit these changes? (y/N): ")
        if response.lower() != 'y':
            print("❌ Deployment cancelled")
            sys.exit(1)
        
        if not commit_changes():
            sys.exit(1)
    
    # Push to GitHub
    if not push_to_github():
        sys.exit(1)
    
    print("\n🎉 Deployment preparation complete!")
    print("\n📋 Next steps:")
    print("1. Go to https://railway.app")
    print("2. Sign in with GitHub")
    print("3. Create new project from GitHub repo")
    print("4. Add MySQL database")
    print("5. Configure environment variables")
    print("\n📖 See RAILWAY_DEPLOYMENT_GUIDE.md for detailed instructions")

if __name__ == '__main__':
    main()