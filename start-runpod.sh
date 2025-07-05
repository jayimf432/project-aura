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
