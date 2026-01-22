#!/bin/bash
# Quick start script for running gRPC server in development

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "🚀 Starting gRPC Development Server"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Generate gRPC stubs if needed
if [ ! -d "users/grpc_generated/proto" ]; then
    echo "⚙️  Generating gRPC stubs from proto files..."
    bash scripts/generate_grpc_stubs.sh
else
    echo "✓ gRPC stubs already generated"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Create superuser if needed (for testing)
echo "👤 Checking for admin user..."
python manage.py shell -c "
from users.models import User
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin@example.com', 'admin123')
    print('✓ Created admin user: admin@example.com / admin123')
else:
    print('✓ Admin user already exists')
" 2>/dev/null || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "Starting gRPC server on port 50051..."
echo "Press Ctrl+C to stop"
echo ""

# Start gRPC server
python manage.py rungrpc
