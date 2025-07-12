# AutoQuiz API

A Flask API that generates multiple-choice quizzes from text content or uploaded PDF documents.

## Features

- Upload PDF documents and extract their content
- Generate quizzes from text or uploaded documents
- RESTful API with Swagger documentation
- SQLite database for document storage

## Project Structure

```
autoquiz-api/
├── app.py                 # Application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── .gitignore             # Git ignore file
├── README.md              # This documentation
└── autoquiz/              # Main package
    ├── __init__.py        # Package initialization
    ├── extensions.py      # Flask extensions (db)
    ├── models/            # Database models
    │   ├── __init__.py
    │   └── document.py    # Document model
    ├── routes/            # API endpoints
    │   ├── __init__.py
    │   ├── documents.py   # Document endpoints
    │   └── quiz.py        # Quiz generation endpoints
    └── utils/             # Utility functions
        ├── __init__.py
        └── pdf.py         # PDF processing utilities
```

## Setup Instructions

### 1. Create and activate a virtual environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root with the following:

```
# OpenAI API Key
OPENAI_API_KEY=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

# Database Configuration (SQLite)
DATABASE_URI=sqlite:///autoquiz.db

# Application Environment
FLASK_ENV=development
```

### 4. Run the application

```bash
python app.py
```

The application will be available at http://localhost:5000, and the Swagger UI documentation will be available at http://localhost:5000/api/docs.

## API Usage

### Using Swagger UI
Navigate to http://localhost:5000/api/docs to use the interactive API documentation.

### Uploading a PDF Document
1. Use the `POST /api/documents` endpoint
2. Upload a PDF file using the file selector
3. You'll receive a document ID in the response

### Generating a Quiz from a Document
1. Use the `GET /api/quiz/document/{doc_id}` endpoint
2. Enter the document ID from the previous step
3. You'll receive a structured quiz based on the document's content

### Generating a Quiz from Text
1. Use the `POST /api/quiz/generate` endpoint
2. Send a JSON request with the text content:
```json
{
  "text": "Photosynthesis is the process by which green plants convert sunlight into chemical energy."
}
```

### Example curl commands

```bash
# Generate quiz from text
curl -X POST http://localhost:5000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Photosynthesis is the process by which green plants convert sunlight into chemical energy."}'

# Upload PDF document
curl -X POST http://localhost:5000/api/documents \
  -F "file=@/path/to/your/document.pdf"

# Generate quiz from document
curl -X GET http://localhost:5000/api/quiz/document/1
```

## Development Notes

- Using OpenAI's GPT-3.5 Turbo model for quiz generation
- SQLite database for document storage (can be upgraded to MySQL if needed)
- The project includes $20 of OpenAI API credit which should be sufficient for testing

## Troubleshooting

- If you encounter issues with the OpenAI API, check that your API key is correctly set in the `.env` file
- For PDF extraction issues, ensure you have the necessary dependencies installed
- For database issues, check that the SQLite database file (autoquiz.db) is being created in the project root
