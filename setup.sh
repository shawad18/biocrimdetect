#!/bin/bash
set -e
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "Upgrading pip..."
pip install --upgrade pip
echo "Installing requirements..."
pip install -r requirements.txt
echo "Initializing database..."
python3 database/init_db.py
echo "Training face encodings (if face images exist)..."
python3 facial_recognition/train_model.py || true
echo "Setup complete. Activate venv with: source venv/bin/activate"
