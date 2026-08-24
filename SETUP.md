# MatchMind AI - Setup Guide

Complete setup instructions for local development.

## Prerequisites

### Required Software
- **Docker Desktop** (version 20.10+)
  - [Download for Mac](https://docs.docker.com/desktop/mac/install/)
  - [Download for Windows](https://docs.docker.com/desktop/windows/install/)
  - [Download for Linux](https://docs.docker.com/desktop/linux/install/)
- **Git** (version 2.30+)
- **Text Editor** (VS Code recommended)

### System Requirements
- **RAM**: Minimum 8GB (16GB recommended for ML models)
- **Disk Space**: At least 5GB free
- **OS**: macOS, Windows 10/11, or Linux

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd MatchMind-AI
```

### 2. Environment Configuration

Create environment files from templates:

```bash
# Root directory
cp .env.example .env

# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env
```

Edit the `.env` files with your configuration. See **Environment Variables** section below.

### 3. Start the Application

#### Using Docker (Recommended)

**Option 1: Automated Setup (Easiest)**
```bash
# Run the setup script
bash scripts/setup.sh

# Or use Make
make setup
```

**Option 2: Manual Setup**
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d
```

First startup will take 5-10 minutes as it:
- Downloads Docker images
- Installs Python/Node dependencies
- Downloads AI models (~420MB)
- Runs database migrations

**Quick Commands with Make:**
```bash
make help           # Show all available commands
make up             # Start services
make down           # Stop services
make logs           # View logs
make migrate        # Run migrations
make createsuperuser # Create admin user
```

#### Without Docker (Manual Setup)

See **Manual Installation** section below.

### 4. Verify Installation

Once all services are running:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **API Docs**: http://localhost:8000/api/docs
- **Django Admin**: http://localhost:8000/admin

### 5. Create Superuser

```bash
docker-compose exec backend python manage.py createsuperuser
```

Follow the prompts to create an admin account.

## Environment Variables

### Backend (.env)

```bash
# Django
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://matchmind:password@db:5432/matchmind_db

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=1440  # minutes (24 hours)

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# File Upload
MAX_UPLOAD_SIZE=5242880  # 5MB in bytes

# AI Models
SENTENCE_TRANSFORMER_MODEL=all-mpnet-base-v2
SPACY_MODEL=en_core_web_sm
```

### Frontend (.env)

```bash
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=MatchMind AI
VITE_MAX_FILE_SIZE=5242880
```

## Docker Commands

### Basic Operations

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes (deletes database!)
docker-compose down -v

# View logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Restart a service
docker-compose restart backend
```

### Development Commands

```bash
# Run Django management commands
docker-compose exec backend python manage.py <command>

# Run migrations
docker-compose exec backend python manage.py migrate

# Create migrations
docker-compose exec backend python manage.py makemigrations

# Access Django shell
docker-compose exec backend python manage.py shell

# Access database
docker-compose exec db psql -U matchmind -d matchmind_db

# Install new Python package
docker-compose exec backend pip install <package>
docker-compose exec backend pip freeze > requirements.txt

# Install new npm package
docker-compose exec frontend npm install <package>

# Run tests
docker-compose exec backend pytest
docker-compose exec frontend npm test
```

### Rebuilding

```bash
# Rebuild specific service
docker-compose build backend

# Rebuild all services
docker-compose build

# Rebuild and start
docker-compose up --build
```

## Manual Installation

If you prefer not to use Docker:

### Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Set up database (install PostgreSQL first)
createdb matchmind_db

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### PostgreSQL Installation

**macOS (Homebrew)**:
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install postgresql-15
sudo systemctl start postgresql
```

**Windows**: Download from [postgresql.org](https://www.postgresql.org/download/windows/)

## Troubleshooting

### Port Already in Use

If ports 5173, 8000, or 5432 are in use:

```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or change port in docker-compose.yml
```

### Docker Build Fails

```bash
# Clear Docker cache
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
```

### AI Model Download Issues

If sentence transformers model fails to download:

```bash
# Manually download model
docker-compose exec backend python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-mpnet-base-v2')"
```

### Database Connection Errors

```bash
# Check database service is running
docker-compose ps db

# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

### Permission Denied Errors (Linux)

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, then test
docker ps
```

### Frontend Not Hot Reloading

```bash
# Rebuild frontend service
docker-compose build frontend
docker-compose up -d frontend

# Or use polling mode (edit vite.config.ts)
```

## Development Workflow

### Branch Strategy

1. Create feature branch: `git checkout -b task-N-description`
2. Make changes and commit
3. Push: `git push -u origin task-N-description`
4. Create pull request or merge to main

### Running Tests

```bash
# Backend tests with coverage
docker-compose exec backend pytest --cov

# Frontend tests
docker-compose exec frontend npm test

# E2E tests (when implemented)
docker-compose exec frontend npm run test:e2e
```

### Code Quality

```bash
# Python linting
docker-compose exec backend flake8
docker-compose exec backend black --check .

# Python formatting
docker-compose exec backend black .

# TypeScript checking
docker-compose exec frontend npm run type-check

# Linting
docker-compose exec frontend npm run lint
```

## Next Steps

1. ✅ Verify all services are running
2. ✅ Create superuser account
3. ✅ Access frontend and create user account
4. ✅ Upload a test resume
5. ✅ Create a job posting
6. ✅ Run your first analysis

See [API_CONTRACT.md](API_CONTRACT.md) for API documentation.

## Getting Help

- Check [Troubleshooting](#troubleshooting) section
- Review Docker logs: `docker-compose logs`
- Open an issue on GitHub
- See [ARCHITECTURE.md](ARCHITECTURE.md) for system design

## Performance Tips

- **First Run**: Allow 10 minutes for model downloads
- **Subsequent Runs**: Should start in 30-60 seconds
- **AI Analysis**: Takes 5-10 seconds per resume/job pair
- **Model Caching**: Models cached in Docker volume for faster restarts

## Security Notes

⚠️ **Development Only**: These settings are for local development.

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Secure SECRET_KEY generation
- DEBUG=False
- HTTPS configuration
- Database security
- CORS configuration
- Rate limiting
