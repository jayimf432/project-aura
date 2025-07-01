#!/bin/bash

echo "🚀 Setting up Project Aura for Mac M1..."
echo "🌟 Welcome to Project Aura Setup (M1 Optimized)"
echo "================================================"

# Check if we're on Mac M1
if [[ $(uname -m) != "arm64" ]]; then
    echo "[WARNING] This script is optimized for Mac M1/M2. You're running on $(uname -m)"
fi

echo "[INFO] Checking system requirements..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "[SUCCESS] Python $PYTHON_VERSION found"
else
    echo "[ERROR] Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "[SUCCESS] Node.js $NODE_VERSION found"
else
    echo "[ERROR] Node.js not found. Please install Node.js 16+"
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "[SUCCESS] npm $NPM_VERSION found"
else
    echo "[ERROR] npm not found"
    exit 1
fi

# Check Docker (optional)
if command -v docker &> /dev/null; then
    echo "[SUCCESS] Docker found"
else
    echo "[WARNING] Docker not found - containerized deployment will not be available"
fi

echo "[INFO] Setting up backend..."

# Create virtual environment
if [ ! -d "backend/venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv backend/venv
fi

# Activate virtual environment
echo "[INFO] Activating virtual environment..."
source backend/venv/bin/activate

# Upgrade pip
echo "[INFO] Upgrading pip..."
pip install --upgrade pip wheel setuptools

# Install PyTorch for M1 first
if ! python -c "import torch" &> /dev/null; then
    echo "[INFO] Installing PyTorch for Apple Silicon..."
    pip install torch torchvision torchaudio
else
    echo "[INFO] PyTorch already installed. Skipping."
fi

# Install other Python dependencies (torch/vision/audio are commented out in requirements-m1.txt)
echo "[INFO] Installing Python dependencies..."
pip install -r backend/requirements-m1.txt

# Ensure uvicorn is installed in the venv
if ! python -c "import uvicorn" &> /dev/null; then
    echo "[INFO] Installing uvicorn in the virtual environment..."
    pip install uvicorn
fi

# Create necessary directories
echo "[INFO] Creating necessary directories..."
mkdir -p backend/uploads backend/outputs backend/temp backend/models

echo "[SUCCESS] Backend setup completed"

echo "[INFO] Setting up frontend..."

# Install Node.js dependencies
echo "[INFO] Installing Node.js dependencies..."
cd frontend
npm install
cd ..

echo "[SUCCESS] Frontend setup completed"

# Create environment files
echo "[INFO] Creating environment files..."

# Backend .env
cat > backend/.env << EOF
# Project Aura Backend Configuration
APP_NAME=Project Aura
APP_VERSION=1.0.0
DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload
MAX_FILE_SIZE=104857600  # 100MB
UPLOAD_DIR=./uploads
OUTPUT_DIR=./outputs
TEMP_DIR=./temp

# AI Models
MODEL_CACHE_DIR=./models
USE_GPU=false  # Set to true if you have GPU support

# Database (optional)
DATABASE_URL=sqlite:///./aura.db

# Redis (optional)
REDIS_URL=redis://localhost:6379

# External APIs
OPENAI_API_KEY=your-openai-api-key
HUGGINGFACE_TOKEN=your-huggingface-token

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/aura.log
EOF

# Frontend .env
cat > frontend/.env << EOF
# Project Aura Frontend Configuration
VITE_APP_NAME=Project Aura
VITE_APP_VERSION=1.0.0
VITE_API_BASE_URL=http://localhost:8000
VITE_API_VERSION=v1
EOF

echo "[SUCCESS] Environment files created"

# Create development scripts
echo "[INFO] Creating development scripts..."

# Start backend script
cat > start-backend.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Project Aura Backend..."
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF

# Start frontend script
cat > start-frontend.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Project Aura Frontend..."
cd frontend
npm run dev
EOF

# Start both script
cat > start-dev.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Project Aura development environment..."

# Function to cleanup background processes
cleanup() {
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend
echo "Starting backend..."
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 2

# Start frontend
echo "Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Development environment started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/docs"
echo "Press Ctrl+C to stop both services"

# Wait for both processes
wait
EOF

# Make scripts executable
chmod +x start-backend.sh start-frontend.sh start-dev.sh

echo "[SUCCESS] Created development scripts"

echo ""
echo "🎉 Project Aura setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Review and update environment files in backend/.env and frontend/.env"
echo "2. Start development environment: ./start-dev.sh"
echo "3. Or start services individually:"
echo "   - Backend: ./start-backend.sh"
echo "   - Frontend: ./start-frontend.sh"
echo ""
echo "Access your application:"
echo "• Frontend: http://localhost:5173"
echo "• Backend API: http://localhost:8000"
echo "• API Documentation: http://localhost:8000/docs"
echo ""
echo "Happy coding! 🚀" 