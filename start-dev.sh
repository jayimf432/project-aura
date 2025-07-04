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
