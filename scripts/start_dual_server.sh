#!/bin/bash
# Start both REST API (gunicorn) and gRPC servers for production

set -e

echo "🚀 Starting Django User Service - Dual Server Mode"
echo "=================================================="
echo ""

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Start REST API server in background
echo "🌐 Starting REST API server on port 8000..."
gunicorn user_service.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --threads 2 \
    --access-logfile - \
    --error-logfile - \
    &

REST_PID=$!
echo "✓ REST API server started (PID: $REST_PID)"

# Start gRPC server in background
echo "⚡ Starting gRPC server on port 50051..."
python manage.py rungrpc --port 50051 --workers 10 &
GRPC_PID=$!
echo "✓ gRPC server started (PID: $GRPC_PID)"

echo ""
echo "🎉 Both servers running!"
echo "   REST API: http://0.0.0.0:8000"
echo "   gRPC:     0.0.0.0:50051"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $REST_PID $GRPC_PID 2>/dev/null || true
    wait $REST_PID $GRPC_PID 2>/dev/null || true
    echo "✓ Servers stopped"
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup INT TERM

# Wait for both processes
wait $REST_PID $GRPC_PID
