Write-Host 'Creating virtual environment...'
python -m venv venv
Write-Host 'Activating venv and installing requirements...'
& .\venv\Scripts\Activate.ps1
Write-Host 'Upgrading pip...'
python -m pip install --upgrade pip

Write-Host 'Installing basic dependencies...'
python -m pip install flask
python -m pip install numpy
python -m pip install pillow
python -m pip install bcrypt
python -m pip install opencv-python

Write-Host 'Initializing database...'
try {
    python .\database\init_db.py
} catch {
    Write-Host 'Warning: Database initialization failed, but continuing setup...'
}

Write-Host ''
Write-Host 'Setup partially complete.'
Write-Host ''
Write-Host 'NOTE: Face recognition components were not installed due to dlib compilation issues.'
Write-Host 'To manually install face recognition components, you will need:'
Write-Host '  1. Visual C++ Build Tools'
Write-Host '  2. Then run: pip install dlib face_recognition'
Write-Host ''
Write-Host 'Activate the virtual environment with: .\venv\Scripts\Activate.ps1'
