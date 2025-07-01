#!/bin/bash

# Project Aura Setup Script
echo "🚀 Setting up Project Aura..."

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
        print_error "Node.js 18+ is required but not installed"
        exit 1
    fi
    
    # Check npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_success "npm $NPM_VERSION found"
    else
        print_error "npm is required but not installed"
        exit 1
    fi
    
    # Check Docker (optional)
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        print_success "Docker $DOCKER_VERSION found"
    else
        print_warning "Docker not found - containerized deployment will not be available"
    fi
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
    
    # Install dependencies
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

# Create environment files
create_env_files() {
    print_status "Creating environment files..."
    
    # Backend .env
    if [ ! -f "backend/.env" ]; then
        cat > backend/.env << EOF
# Project Aura Backend Environment Variables
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000

# CORS Settings
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

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
        print_success "Created backend/.env"
    fi
    
    # Frontend .env
    if [ ! -f "frontend/.env" ]; then
        cat > frontend/.env << EOF
# Project Aura Frontend Environment Variables
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Project Aura
VITE_APP_VERSION=1.0.0
EOF
        print_success "Created frontend/.env"
    fi
}

# Create development scripts
create_scripts() {
    print_status "Creating development scripts..."
    
    # Start backend script
    cat > start-backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF
    chmod +x start-backend.sh
    
    # Start frontend script
    cat > start-frontend.sh << 'EOF'
#!/bin/bash
cd frontend
npm run dev
EOF
    chmod +x start-frontend.sh
    
    # Start both script
    cat > start-dev.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Project Aura development environment..."

# Start backend in background
echo "Starting backend..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Development environment started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for user to stop
wait

# Cleanup
echo "🛑 Stopping services..."
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
echo "✅ Services stopped"
EOF
    chmod +x start-dev.sh
    
    print_success "Created development scripts"
}

# Main setup function
main() {
    echo "🌟 Welcome to Project Aura Setup"
    echo "=================================="
    
    # Check requirements
    check_requirements
    
    # Setup backend
    setup_backend
    
    # Setup frontend
    setup_frontend
    
    # Create environment files
    create_env_files
    
    # Create development scripts
    create_scripts
    
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
}

# Run main function
main 