#!/bin/bash
echo "🚀 Starting Project Aura Frontend on RunPod..."

# Get port from environment or use default
PORT=${FRONTEND_PORT:-5173}

cd frontend

echo "Starting frontend on port $PORT..."
npm run dev -- --host 0.0.0.0 --port $PORT
