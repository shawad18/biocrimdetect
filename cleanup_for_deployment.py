#!/usr/bin/env python3
"""
Cleanup Script for Railway Deployment
Removes unnecessary files and optimizes the project for production deployment.
"""

import os
import shutil
import glob

def remove_cache_files():
    """Remove Python cache files"""
    print("🧹 Removing cache files...")
    
    # Remove __pycache__ directories
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(cache_path)
            print(f"   Removed: {cache_path}")
    
    # Remove .pyc files
    pyc_files = glob.glob('**/*.pyc', recursive=True)
    for pyc_file in pyc_files:
        os.remove(pyc_file)
        print(f"   Removed: {pyc_file}")
    
    print("✅ Cache files cleaned")

def remove_development_files():
    """Remove development-only files"""
    print("🧹 Removing development files...")
    
    dev_files = [
        '.DS_Store',
        'Thumbs.db',
        '*.tmp',
        '*.temp',
        '*.log',
        'debug.log',
        'error.log'
    ]
    
    for pattern in dev_files:
        files = glob.glob(pattern, recursive=True)
        for file in files:
            if os.path.exists(file):
                os.remove(file)
                print(f"   Removed: {file}")
    
    print("✅ Development files cleaned")

def optimize_static_files():
    """Check static files for optimization"""
    print("📁 Checking static files...")
    
    static_dir = 'static'
    if os.path.exists(static_dir):
        # Count files
        css_files = glob.glob(os.path.join(static_dir, '**/*.css'), recursive=True)
        js_files = glob.glob(os.path.join(static_dir, '**/*.js'), recursive=True)
        img_files = glob.glob(os.path.join(static_dir, '**/*.{png,jpg,jpeg,gif,svg}'), recursive=True)
        
        print(f"   CSS files: {len(css_files)}")
        print(f"   JS files: {len(js_files)}")
        print(f"   Image files: {len(img_files)}")
        
        # Check for large files
        large_files = []
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                if size > 1024 * 1024:  # 1MB
                    large_files.append((file_path, size))
        
        if large_files:
            print("   ⚠️  Large files found:")
            for file_path, size in large_files:
                print(f"      {file_path}: {size / (1024*1024):.1f}MB")
        else:
            print("   ✅ No large files found")
    
    print("✅ Static files checked")

def check_requirements():
    """Verify requirements.txt"""
    print("📦 Checking requirements.txt...")
    
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        print(f"   Total packages: {len(requirements)}")
        
        # Check for development packages
        dev_packages = ['pytest', 'black', 'flake8', 'mypy', 'coverage']
        found_dev = [pkg for pkg in requirements if any(dev in pkg.lower() for dev in dev_packages)]
        
        if found_dev:
            print("   ⚠️  Development packages found:")
            for pkg in found_dev:
                print(f"      {pkg}")
        else:
            print("   ✅ No development packages found")
    else:
        print("   ❌ requirements.txt not found")
    
    print("✅ Requirements checked")

def verify_deployment_files():
    """Verify all deployment files are present"""
    print("📋 Verifying deployment files...")
    
    required_files = {
        'app.py': 'Main Flask application',
        'requirements.txt': 'Python dependencies',
        'Procfile': 'Railway process configuration',
        'runtime.txt': 'Python version specification',
        '.gitignore': 'Git ignore rules'
    }
    
    missing_files = []
    for file, description in required_files.items():
        if os.path.exists(file):
            print(f"   ✅ {file} - {description}")
        else:
            print(f"   ❌ {file} - {description} (MISSING)")
            missing_files.append(file)
    
    if missing_files:
        print(f"   ⚠️  Missing files: {', '.join(missing_files)}")
    else:
        print("   ✅ All deployment files present")
    
    print("✅ Deployment files verified")

def show_deployment_summary():
    """Show deployment summary"""
    print("\n" + "=" * 50)
    print("🚂 RAILWAY DEPLOYMENT SUMMARY")
    print("=" * 50)
    
    # Project size
    total_size = 0
    file_count = 0
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
            file_count += 1
    
    print(f"📊 Project Statistics:")
    print(f"   Total files: {file_count}")
    print(f"   Total size: {total_size / (1024*1024):.1f}MB")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Run: git add .")
    print(f"   2. Run: git commit -m 'Prepare for Railway deployment'")
    print(f"   3. Run: git push origin main")
    print(f"   4. Deploy to Railway: https://railway.app")
    
    print(f"\n📖 Documentation:")
    print(f"   - RAILWAY_DEPLOYMENT_GUIDE.md")
    print(f"   - .env.railway (environment variables template)")
    
    print(f"\n🎉 Project is ready for Railway deployment!")

def main():
    """Main cleanup function"""
    print("🚂 Railway Deployment Cleanup")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Run this script from the project root.")
        return
    
    # Perform cleanup
    remove_cache_files()
    remove_development_files()
    optimize_static_files()
    check_requirements()
    verify_deployment_files()
    show_deployment_summary()

if __name__ == '__main__':
    main()