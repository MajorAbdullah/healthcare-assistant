#!/bin/bash

# Healthcare Assistant - API Server Startup Script

echo "========================================"
echo "🏥 Healthcare Assistant - API Server"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements_healthcare.txt

echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "📡 Starting API server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔌 WebSocket Chat: ws://localhost:8000/ws/chat/{user_id}"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

# Start the FastAPI server
cd api
python3 main.py
