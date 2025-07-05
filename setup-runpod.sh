#!/bin/bash

# Project Aura Setup Script for RunPod
echo "🚀 Setting up Project Aura on RunPod..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3.9+ is required but not installed"
        exit 1
    fi
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version | cut -d'v' -f2)
        print_success "Node.js $NODE_VERSION found"
    else
        print_warning "Node.js not found - installing..."
        # Install Node.js for RunPod
        curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
        apt-get install -y nodejs
        print_success "Node.js installed"
    fi
    
    # Check npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_success "npm $NPM_VERSION found"
    else
        print_error "npm not found"
        exit 1
    fi
    
    # Check CUDA
    if command -v nvidia-smi &> /dev/null; then
        CUDA_VERSION=$(nvidia-smi | grep "CUDA Version" | cut -d' ' -f9)
        print_success "CUDA $CUDA_VERSION found"
    else
        print_warning "CUDA not detected - will use CPU mode"
    fi
    
    # Check Docker (optional)
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        print_success "Docker $DOCKER_VERSION found"
    else
        print_warning "Docker not found - containerized deployment will not be available"
    fi
}

# Install system dependencies for RunPod
install_system_deps() {
    print_status "Installing system dependencies for RunPod..."
    
    # Update package list
    apt-get update
    
    # Install essential packages
    apt-get install -y \
        build-essential \
        curl \
        git \
        wget \
        unzip \
        software-properties-common \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libgomp1 \
        ffmpeg \
        libavcodec-extra \
        libavformat-dev \
        libswscale-dev \
        libavutil-dev \
        libavfilter-dev \
        libavdevice-dev
    
    print_success "System dependencies installed"
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install PyTorch with CUDA support for RunPod
    print_status "Installing PyTorch with CUDA support..."
    if command -v nvidia-smi &> /dev/null; then
        # Install PyTorch with CUDA
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
        print_success "PyTorch with CUDA installed"
    else
        # Install CPU-only PyTorch
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
        print_warning "PyTorch CPU-only installed (no GPU detected)"
    fi
    
    # Install other dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Create necessary directories
    print_status "Creating necessary directories..."
    mkdir -p uploads outputs temp
    
    cd ..
    print_success "Backend setup completed"
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    cd ..
    print_success "Frontend setup completed"
}

# Create environment files for RunPod
create_env_files() {
    print_status "Creating environment files for RunPod..."
    
    # Get RunPod port from environment or use defaults
    RUNPOD_PORT=${RUNPOD_PORT:-8000}
    FRONTEND_PORT=${FRONTEND_PORT:-5173}
    
    # Backend .env
    if [ ! -f "backend/.env" ]; then
        cat > backend/.env << EOF
# Project Aura Backend Environment Variables for RunPod
ENVIRONMENT=production
DEBUG=false
HOST=0.0.0.0
PORT=${RUNPOD_PORT}

# CORS Settings for RunPod
CORS_ORIGINS=http://localhost:${FRONTEND_PORT},http://127.0.0.1:${FRONTEND_PORT},http://0.0.0.0:${FRONTEND_PORT}

# File Upload Settings
MAX_FILE_SIZE=104857600
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs
TEMP_DIR=temp

# AI Model Settings
DIFFUSION_MODEL_ID=runwayml/stable-diffusion-v1-5
CONTROLNET_MODEL_ID=lllyasviel/control_v11p_sd15_canny
LLM_MODEL_ID=gpt2

# Video Processing Settings
MAX_VIDEO_DURATION=60
TARGET_FPS=30
MAX_RESOLUTION=1920,1080

# Security
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs (optional)
OPENAI_API_KEY=
HUGGINGFACE_API_KEY=
EOF
        print_success "Created backend/.env for RunPod"
    fi
    
    # Frontend .env
    if [ ! -f "frontend/.env" ]; then
        cat > frontend/.env << EOF
# Project Aura Frontend Environment Variables for RunPod
VITE_API_URL=http://localhost:${RUNPOD_PORT}
VITE_APP_NAME=Project Aura
VITE_APP_VERSION=1.0.0
EOF
        print_success "Created frontend/.env for RunPod"
    fi
}

# Create RunPod-specific scripts
create_runpod_scripts() {
    print_status "Creating RunPod-specific scripts..."
    
    # Start backend script for RunPod
    cat > start-backend-runpod.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Project Aura Backend on RunPod..."

# Get port from environment or use default
PORT=${RUNPOD_PORT:-8000}

cd backend
source venv/bin/activate

# Set environment variables for production
export ENVIRONMENT=production
export DEBUG=false
export HOST=0.0.0.0
export PORT=$PORT

echo "Starting backend on port $PORT..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
EOF
    chmod +x start-backend-runpod.sh
    
    # Start frontend script for RunPod
    cat > start-frontend-runpod.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Project Aura Frontend on RunPod..."

# Get port from environment or use default
PORT=${FRONTEND_PORT:-5173}

cd frontend

echo "Starting frontend on port $PORT..."
npm run dev -- --host 0.0.0.0 --port $PORT
EOF
    chmod +x start-frontend-runpod.sh
    
    # Start both script for RunPod
    cat > start-runpod.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Project Aura on RunPod..."

# Get ports from environment or use defaults
BACKEND_PORT=${RUNPOD_PORT:-8000}
FRONTEND_PORT=${FRONTEND_PORT:-5173}

echo "Backend port: $BACKEND_PORT"
echo "Frontend port: $FRONTEND_PORT"

# Start backend in background
echo "Starting backend..."
cd backend
source venv/bin/activate
export ENVIRONMENT=production
export DEBUG=false
export HOST=0.0.0.0
export PORT=$BACKEND_PORT
uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT --workers 1 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 5

# Start frontend
echo "Starting frontend..."
cd ../frontend
npm run dev -- --host 0.0.0.0 --port $FRONTEND_PORT &
FRONTEND_PID=$!

echo "✅ Project Aura started on RunPod!"
echo "Backend: http://localhost:$BACKEND_PORT"
echo "Frontend: http://localhost:$FRONTEND_PORT"
echo "API Docs: http://localhost:$BACKEND_PORT/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for user to stop
wait

# Cleanup
echo "🛑 Stopping services..."
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
echo "✅ Services stopped"
EOF
    chmod +x start-runpod.sh
    
    print_success "Created RunPod-specific scripts"
}

# Main setup function
main() {
    echo "🌟 Welcome to Project Aura RunPod Setup"
    echo "========================================"
    
    # Check requirements
    check_requirements
    
    # Install system dependencies
    install_system_deps
    
    # Setup backend
    setup_backend
    
    # Setup frontend
    setup_frontend
    
    # Create environment files
    create_env_files
    
    # Create RunPod-specific scripts
    create_runpod_scripts
    
    echo ""
    echo "🎉 Project Aura RunPod setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Review and update environment files in backend/.env and frontend/.env"
    echo "2. Start the application: ./start-runpod.sh"
    echo "3. Or start services individually:"
    echo "   - Backend: ./start-backend-runpod.sh"
    echo "   - Frontend: ./start-frontend-runpod.sh"
    echo ""
    echo "RunPod Configuration:"
    echo "• Backend port: \${RUNPOD_PORT:-8000}"
    echo "• Frontend port: \${FRONTEND_PORT:-5173}"
    echo "• Set these environment variables in RunPod if needed"
    echo ""
    echo "Access your application:"
    echo "• Frontend: http://localhost:\${FRONTEND_PORT:-5173}"
    echo "• Backend API: http://localhost:\${RUNPOD_PORT:-8000}"
    echo "• API Documentation: http://localhost:\${RUNPOD_PORT:-8000}/docs"
    echo ""
    echo "Happy coding on RunPod! 🚀"
}

# Run main function
main 