# MatchMind AI - Backend

Django REST API for the MatchMind AI application.

## Project Structure

```
backend/
├── config/              # Django project configuration
│   ├── settings.py     # Main settings
│   ├── urls.py         # URL routing
│   ├── wsgi.py         # WSGI configuration
│   └── asgi.py         # ASGI configuration
├── users/              # User authentication and management
├── resumes/            # Resume upload and management
├── jobs/               # Job description and tracking
├── analysis/           # AI analysis engine
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── Dockerfile          # Docker configuration
```

## Apps

### Users App
- Custom user model with email-based authentication
- JWT token authentication
- User profile management

### Resumes App
- PDF resume upload and storage
- Text extraction from PDFs
- Skill extraction
- Resume version management

### Jobs App
- Job description storage
- Application status tracking
- Job skill extraction

### Analysis App
- Resume-job compatibility analysis
- Semantic similarity scoring
- Skill gap identification
- Improvement suggestions

## Database Models

### User
- Email-based authentication
- First name, last name
- Related: resumes, jobs, analyses

### Resume
- User-uploaded PDF files
- Extracted text and skills
- File metadata

### Job
- Job title, company, description
- Application status tracking
- Extracted skills
- Notes

### Analysis
- Resume-job pair analysis
- Match score, semantic similarity
- Matching and missing skills
- Keyword analysis
- Improvement suggestions

## Running Locally

### With Docker (Recommended)
```bash
# From project root
docker-compose up backend

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

### Without Docker
```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

## Common Commands

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
pytest

# Run with coverage
pytest --cov

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

## API Endpoints

API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

### Main Endpoints
- `/api/auth/` - Authentication (login, register, profile)
- `/api/resumes/` - Resume management
- `/api/jobs/` - Job tracking
- `/api/analysis/` - AI analysis

## Configuration

All configuration is done through environment variables. See `.env.example` for available options.

### Key Settings
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated allowed hosts
- `DB_*` - Database configuration
- `JWT_*` - JWT token settings
- `CORS_ALLOWED_ORIGINS` - CORS origins
- `MAX_UPLOAD_SIZE` - Maximum file upload size
- `SENTENCE_TRANSFORMER_MODEL` - AI model name
- `SPACY_MODEL` - spaCy model name

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific app
pytest users/

# Run specific test
pytest users/tests.py::TestUserModel
```

## Development Notes

- Custom user model uses email instead of username
- All models have proper indexes for performance
- File uploads are validated for size and type
- JWT tokens expire after configured time
- CORS is configured for frontend origins

## Next Steps

After Task 3:
- Task 4: Implement authentication endpoints
- Task 6: Implement resume upload and CRUD
- Task 8: Implement job management
- Task 10-13: Implement AI analysis engine
