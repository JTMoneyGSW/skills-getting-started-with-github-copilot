# GitHub Copilot Instructions for Mergington High School Activities API

## Architecture Overview
This is a FastAPI-based web application serving a simple extracurricular activities management system for Mergington High School. The backend provides REST API endpoints while serving static frontend files. All data is stored in-memory using Python dictionaries, resetting on server restart.

Key components:
- **Backend**: `src/app.py` - FastAPI app with activity data and signup logic
- **Frontend**: `src/static/` - Vanilla JavaScript app fetching from API
- **Data Model**: Activities use name as primary key; students identified by email

## API Patterns
- Activities accessed via name in URL paths (e.g., `/activities/Basketball%20Team/signup`)
- Signup uses query parameter for email: `POST /activities/{activity_name}/signup?email=user@mergington.edu`
- Root endpoint redirects to static HTML: `GET /` → `/static/index.html`

## Data Structures
Activities dict structure (from `src/app.py`):
```python
{
    "activity_name": {
        "description": str,
        "schedule": str,
        "max_participants": int,
        "participants": [email1, email2, ...]
    }
}
```

## Development Workflow
- **Run server**: `python src/app.py` (assumes uvicorn run code added)
- **Dependencies**: Install from `requirements.txt` (FastAPI + Uvicorn)
- **Testing**: Use pytest with `pythonpath = .` configured in `pytest.ini`
- **Static serving**: Files in `src/static/` auto-mounted at `/static` path

## Code Conventions
- Use `pathlib.Path` for file paths (e.g., `Path(__file__).parent`)
- In-memory data manipulation: Direct dict/list operations for participants
- Error handling: FastAPI HTTPException for invalid activities
- Frontend: Async/await for API calls, DOM manipulation for dynamic content

## Common Patterns
- Activity iteration: `Object.entries(activities).forEach(([name, details]) => ...)`
- Form submission: Prevent default, encode URI components for activity names
- Response handling: Check `response.ok`, display messages with auto-hide timers

Reference: `src/README.md` for API endpoints and data model details.