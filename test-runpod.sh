#!/bin/bash

# Test script for RunPod setup
echo "🧪 Testing Project Aura RunPod Setup..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to test components
test_component() {
    local name=$1
    local command=$2
    local description=$3
    
    echo -n "Testing $name... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo "  $description"
        return 1
    fi
}

# Test Python
test_component "Python" "python3 --version" "Python 3.9+ required"

# Test Node.js
test_component "Node.js" "node --version" "Node.js 18+ required"

# Test npm
test_component "npm" "npm --version" "npm required for frontend"

# Test CUDA
if command -v nvidia-smi &> /dev/null; then
    test_component "CUDA" "nvidia-smi" "CUDA for GPU acceleration"
else
    echo -e "${YELLOW}⚠️  CUDA not detected - will use CPU mode${NC}"
fi

# Test backend virtual environment
if [ -d "backend/venv" ]; then
    test_component "Backend venv" "test -d backend/venv" "Backend virtual environment exists"
else
    echo -e "${YELLOW}⚠️  Backend virtual environment not found - run setup-runpod.sh first${NC}"
fi

# Test frontend node_modules
if [ -d "frontend/node_modules" ]; then
    test_component "Frontend deps" "test -d frontend/node_modules" "Frontend dependencies installed"
else
    echo -e "${YELLOW}⚠️  Frontend dependencies not found - run setup-runpod.sh first${NC}"
fi

# Test environment files
test_component "Backend .env" "test -f backend/.env" "Backend environment file exists"
test_component "Frontend .env" "test -f frontend/.env" "Frontend environment file exists"

# Test RunPod scripts
test_component "RunPod scripts" "test -f start-runpod.sh" "RunPod start script exists"
test_component "Backend script" "test -f start-backend-runpod.sh" "Backend start script exists"
test_component "Frontend script" "test -f start-frontend-runpod.sh" "Frontend start script exists"

# Test PyTorch installation (if venv exists)
if [ -d "backend/venv" ]; then
    cd backend
    source venv/bin/activate
    if python -c "import torch; print('PyTorch version:', torch.__version__)" 2>/dev/null; then
        echo -e "${GREEN}✅ PyTorch installed${NC}"
        
        # Test CUDA availability
        if python -c "import torch; print('CUDA available:', torch.cuda.is_available())" 2>/dev/null; then
            echo -e "${GREEN}✅ CUDA availability checked${NC}"
        fi
    else
        echo -e "${RED}❌ PyTorch not installed${NC}"
    fi
    cd ..
fi

echo ""
echo "🎯 RunPod Setup Test Complete!"
echo ""
echo "If all tests passed, you can start the application with:"
echo "  ./start-runpod.sh"
echo ""
echo "If some tests failed, run the setup script first:"
echo "  ./setup-runpod.sh" 