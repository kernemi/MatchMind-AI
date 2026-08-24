#!/bin/bash
# MatchMind AI - Initial Setup Script

echo "🧠 MatchMind AI - Setup Script"
echo "================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install it first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Create .env files if they don't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env from template..."
    cp backend/.env.example backend/.env
fi

if [ ! -f frontend/.env ]; then
    echo "📝 Creating frontend/.env from template..."
    cp frontend/.env.example frontend/.env
fi

echo "✅ Environment files ready"
echo ""

# Build Docker images
echo "🏗️  Building Docker images (this may take 5-10 minutes)..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed. Please check the error messages above."
    exit 1
fi

echo "✅ Docker images built successfully"
echo ""

# Start services
echo "🚀 Starting services..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start services. Please check the error messages above."
    exit 1
fi

echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "📦 Running database migrations..."
docker-compose exec -T backend python manage.py migrate

if [ $? -ne 0 ]; then
    echo "⚠️  Migrations may have failed. You might need to run them manually."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Create a superuser: docker-compose exec backend python manage.py createsuperuser"
echo "   2. Access the application:"
echo "      - Frontend: http://localhost:5173"
echo "      - Backend API: http://localhost:8000/api"
echo "      - API Docs: http://localhost:8000/api/docs"
echo "      - Django Admin: http://localhost:8000/admin"
echo ""
echo "📚 View logs: docker-compose logs -f"
echo "🛑 Stop services: docker-compose down"
echo ""
