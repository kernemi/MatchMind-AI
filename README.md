# 🧠 MatchMind AI

**AI-Powered Resume & Job Compatibility Analyzer**

MatchMind AI helps job seekers understand how well their resume matches specific job descriptions through advanced AI-powered analysis. Upload your resume, paste a job description, and receive detailed insights on compatibility, skill gaps, and improvement suggestions.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.x-blue.svg)
![Django](https://img.shields.io/badge/django-4.2-green.svg)

## ✨ Features

- 📄 **Resume Management** - Upload and manage multiple resume versions
- 🎯 **AI Match Score** - Get detailed compatibility scores (0-100%)
- ✅ **Skill Analysis** - Identify matching and missing skills
- 🔍 **Keyword Coverage** - Compare important keywords
- 🧠 **Semantic Similarity** - Understand meaning-based matches
- 💡 **Smart Suggestions** - Get actionable improvement recommendations
- 📊 **Job Tracking** - Save and manage job applications with status tracking
- 📈 **Analysis History** - View and compare past analyses
- 📱 **Mobile Responsive** - View results seamlessly on any device

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MatchMind-AI
   ```

2. **Start the application**
   ```bash
   docker-compose up
   ```

3. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/api
   - API Documentation: http://localhost:8000/api/docs

For detailed setup instructions, see [SETUP.md](SETUP.md)

## 🏗️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **React Router** - Client-side routing
- **React Query** - Server state management
- **Axios** - HTTP client

### Backend
- **Django 4.2+** with Python 3.11
- **Django REST Framework** - RESTful API
- **SimpleJWT** - JWT authentication
- **PostgreSQL 15** - Database

### AI/ML
- **Sentence Transformers** - Semantic embeddings (all-mpnet-base-v2)
- **spaCy** - NLP and text processing
- **scikit-learn** - Similarity scoring
- **PyMuPDF** - PDF text extraction

## 📖 Documentation

- [Setup Guide](SETUP.md) - Detailed installation and configuration
- [API Documentation](API_CONTRACT.md) - Complete API reference
- [Architecture](ARCHITECTURE.md) - System design and architecture
- [Deployment Guide](DEPLOYMENT.md) - Production deployment instructions
- [Task List](tasks.md) - Development tasks and progress

## 🎯 How It Works

```
User uploads Resume (PDF) + Job Description
              ↓
    Django REST API receives request
              ↓
       PDF Text Extraction
              ↓
   Text Cleaning & Processing
              ↓
        Skill Extraction
              ↓
     Generate Embeddings
              ↓
  Semantic Similarity Analysis
              ↓
    ┌─────────────────────────┐
    │    AI Analysis Results   │
    │                          │
    │  • Match Score           │
    │  • Matching Skills       │
    │  • Missing Skills        │
    │  • Keyword Analysis      │
    │  • Semantic Similarity   │
    │  • Suggestions           │
    └─────────────────────────┘
```

## 🧪 Testing

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
cd frontend && npm test
```

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using AI, NLP, and modern web technologies**
