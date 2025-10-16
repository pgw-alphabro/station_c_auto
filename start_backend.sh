#!/bin/bash

echo "Starting FastAPI backend server..."
cd backend
pip install -r requirements.txt
python main.py
