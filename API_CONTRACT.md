# MatchMind AI - API Contract

Complete API documentation for MatchMind AI backend services.

## Base URL

```
Development: http://localhost:8000/api
Production: https://your-domain.com/api
```

## Authentication

MatchMind AI uses JWT (JSON Web Token) authentication.

### Authentication Flow

1. Register or login to receive access and refresh tokens
2. Include access token in Authorization header for protected endpoints
3. Refresh access token when expired using refresh token

### Header Format

```
Authorization: Bearer <access_token>
```

---

## API Endpoints

### 🔐 Authentication

#### Register User

**POST** `/auth/register/`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors:**
- `400 Bad Request` - Validation errors (email exists, weak password, etc.)

---

#### Login

**POST** `/auth/login/`

Authenticate user and receive JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Errors:**
- `401 Unauthorized` - Invalid credentials

---

#### Refresh Token

**POST** `/auth/refresh/`

Get new access token using refresh token.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Errors:**
- `401 Unauthorized` - Invalid or expired refresh token

---

#### Get Profile

**GET** `/auth/profile/`

Get current user's profile.

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2024-01-15T10:30:00Z",
  "resume_count": 3,
  "job_count": 5,
  "analysis_count": 8
}
```

---

#### Update Profile

**PUT** `/auth/profile/`

Update user profile information.

**Authentication:** Required

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "email": "newemail@example.com"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "newemail@example.com",
  "first_name": "John",
  "last_name": "Smith",
  "updated_at": "2024-01-16T14:20:00Z"
}
```

---

### 📄 Resume Management

#### List Resumes

**GET** `/resumes/`

Get all resumes for authenticated user.

**Authentication:** Required

**Query Parameters:**
- `ordering` - Sort by field (e.g., `-uploaded_at`, `name`)
- `search` - Search by name

**Response:** `200 OK`
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "name": "Software Engineer Resume",
      "file_size": 245632,
      "uploaded_at": "2024-01-15T10:30:00Z",
      "analysis_count": 5
    },
    {
      "id": 2,
      "name": "Data Science Resume",
      "file_size": 198456,
      "uploaded_at": "2024-01-10T15:20:00Z",
      "analysis_count": 3
    }
  ]
}
```

---

#### Upload Resume

**POST** `/resumes/`

Upload a new resume PDF.

**Authentication:** Required

**Request:** `multipart/form-data`
```
name: "Software Engineer Resume"
file: [PDF file, max 5MB]
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Software Engineer Resume",
  "file": "/media/resumes/user_1/resume_123.pdf",
  "file_size": 245632,
  "extracted_text": "John Doe\nSoftware Engineer...",
  "extracted_skills": ["Python", "Django", "React", "PostgreSQL"],
  "uploaded_at": "2024-01-15T10:30:00Z"
}
```

**Errors:**
- `400 Bad Request` - File too large, invalid PDF, or validation errors
- `413 Payload Too Large` - File exceeds 5MB

---

#### Get Resume

**GET** `/resumes/{id}/`

Get detailed resume information.

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Software Engineer Resume",
  "file": "/media/resumes/user_1/resume_123.pdf",
  "file_size": 245632,
  "extracted_text": "Full resume text content...",
  "extracted_skills": ["Python", "Django", "React", "PostgreSQL", "Docker"],
  "uploaded_at": "2024-01-15T10:30:00Z",
  "analysis_count": 5,
  "last_analyzed": "2024-01-16T09:15:00Z"
}
```

**Errors:**
- `404 Not Found` - Resume not found or not owned by user

---

#### Update Resume

**PUT/PATCH** `/resumes/{id}/`

Update resume name.

**Authentication:** Required

**Request Body:**
```json
{
  "name": "Updated Resume Name"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Updated Resume Name",
  "updated_at": "2024-01-16T11:45:00Z"
}
```

---

#### Delete Resume

**DELETE** `/resumes/{id}/`

Delete a resume and its file.

**Authentication:** Required

**Response:** `204 No Content`

**Errors:**
- `404 Not Found` - Resume not found

---

### 💼 Job Management

#### List Jobs

**GET** `/jobs/`

Get all job postings for authenticated user.

**Authentication:** Required

**Query Parameters:**
- `status` - Filter by status (saved, applied, interviewing, offered, rejected)
- `search` - Search by title or company
- `ordering` - Sort by field

**Response:** `200 OK`
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "title": "Senior Software Engineer",
      "company": "Google",
      "status": "applied",
      "created_at": "2024-01-15T10:30:00Z",
      "analysis_count": 2
    }
  ]
}
```

---

#### Create Job

**POST** `/jobs/`

Save a new job posting.

**Authentication:** Required

**Request Body:**
```json
{
  "title": "Senior Software Engineer",
  "company": "Google",
  "description": "We are looking for a Senior Software Engineer...",
  "url": "https://careers.google.com/jobs/...",
  "status": "saved",
  "notes": "Referred by John Smith"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "Senior Software Engineer",
  "company": "Google",
  "description": "We are looking for...",
  "url": "https://careers.google.com/jobs/...",
  "status": "saved",
  "notes": "Referred by John Smith",
  "extracted_skills": ["Python", "Kubernetes", "AWS", "Microservices"],
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

#### Get Job

**GET** `/jobs/{id}/`

Get detailed job information.

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Senior Software Engineer",
  "company": "Google",
  "description": "Full job description...",
  "url": "https://careers.google.com/jobs/...",
  "status": "applied",
  "notes": "Interview scheduled for next week",
  "extracted_skills": ["Python", "Kubernetes", "AWS"],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:20:00Z",
  "analysis_count": 3
}
```

---

#### Update Job

**PUT/PATCH** `/jobs/{id}/`

Update job information.

**Authentication:** Required

**Request Body:**
```json
{
  "status": "interviewing",
  "notes": "First round interview completed"
}
```

**Response:** `200 OK`

---

#### Delete Job

**DELETE** `/jobs/{id}/`

Delete a job posting.

**Authentication:** Required

**Response:** `204 No Content`

---

### 🧠 Analysis

#### Create Analysis

**POST** `/analysis/`

Analyze resume against job description.

**Authentication:** Required

**Request Body:**
```json
{
  "resume_id": 1,
  "job_id": 1
}
```

**Response:** `201 Created` (processing takes 5-10 seconds)
```json
{
  "id": 1,
  "resume": {
    "id": 1,
    "name": "Software Engineer Resume"
  },
  "job": {
    "id": 1,
    "title": "Senior Software Engineer",
    "company": "Google"
  },
  "match_score": 82.5,
  "semantic_similarity": 0.78,
  "matching_skills": [
    "Python",
    "Django",
    "React",
    "PostgreSQL",
    "Docker"
  ],
  "missing_skills": [
    "Kubernetes",
    "AWS",
    "Microservices"
  ],
  "keyword_analysis": {
    "resume_keywords": {
      "python": 12,
      "django": 8,
      "react": 6
    },
    "job_keywords": {
      "python": 5,
      "kubernetes": 8,
      "aws": 6
    },
    "coverage_score": 65.5
  },
  "suggestions": [
    "Add Kubernetes experience to your resume",
    "Highlight any AWS or cloud platform experience",
    "Include microservices architecture projects",
    "Emphasize Python expertise more prominently"
  ],
  "created_at": "2024-01-16T09:15:00Z"
}
```

**Errors:**
- `400 Bad Request` - Invalid resume_id or job_id
- `404 Not Found` - Resume or job not found

---

#### List Analyses

**GET** `/analysis/`

Get analysis history for authenticated user.

**Authentication:** Required

**Query Parameters:**
- `resume_id` - Filter by resume
- `job_id` - Filter by job
- `ordering` - Sort by field (e.g., `-created_at`, `-match_score`)

**Response:** `200 OK`
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "resume": {
        "id": 1,
        "name": "Software Engineer Resume"
      },
      "job": {
        "id": 1,
        "title": "Senior Software Engineer",
        "company": "Google"
      },
      "match_score": 82.5,
      "created_at": "2024-01-16T09:15:00Z"
    }
  ]
}
```

---

#### Get Analysis

**GET** `/analysis/{id}/`

Get detailed analysis results.

**Authentication:** Required

**Response:** `200 OK` (same structure as Create Analysis response)

---

#### Delete Analysis

**DELETE** `/analysis/{id}/`

Delete an analysis.

**Authentication:** Required

**Response:** `204 No Content`

---

## Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Resource deleted successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required or invalid token |
| 403 | Forbidden - User doesn't have permission |
| 404 | Not Found - Resource not found |
| 413 | Payload Too Large - File exceeds size limit |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |

## Error Response Format

```json
{
  "error": "Error message",
  "detail": "Detailed error description",
  "field_errors": {
    "email": ["This email is already registered"],
    "password": ["Password must be at least 8 characters"]
  }
}
```

## Rate Limiting

- **Anonymous users**: 20 requests/minute
- **Authenticated users**: 100 requests/minute
- **Analysis endpoint**: 10 requests/minute per user

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642334400
```

## File Upload Specifications

### Resume PDF Upload

- **Max Size**: 5MB
- **Accepted Format**: PDF only
- **Mime Types**: `application/pdf`
- **Field Name**: `file`
- **Encoding**: `multipart/form-data`

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20, max: 100)

**Response:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/resumes/?page=2",
  "previous": null,
  "results": [...]
}
```

## CORS

Allowed origins:
- Development: `http://localhost:5173`
- Production: Your production domain

## Interactive API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

## Postman Collection

Import the Postman collection from `postman/MatchMind-AI.postman_collection.json`

### Environment Variables

```
base_url: http://localhost:8000/api
access_token: (automatically set after login)
refresh_token: (automatically set after login)
```

## Webhooks (Future)

Coming in v2.0:
- Analysis completion webhooks
- Application status update notifications

## API Versioning

Current version: `v1` (implicit in base URL)

Future versions will be explicit: `/api/v2/`

## Support

For API issues or questions:
- Check interactive docs at `/api/docs/`
- Review this contract
- Open an issue on GitHub
