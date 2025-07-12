from flask import request
from flask_restx import Namespace, Resource, fields
from autoquiz.models import Document
import os
import re

# Create namespace
ns = Namespace('api/quiz', description='Quiz operations')

# Models for Swagger documentation
quiz_request = ns.model('QuizRequest', {
    'text': fields.String(required=True, description='Input text to generate a quiz from')
})

quiz_question = ns.model('QuizQuestion', {
    'question': fields.String(description='Question text'),
    'options': fields.List(fields.String, description='Answer options'),
    'answer': fields.String(description='Correct answer')
})

quiz_response = ns.model('QuizResponse', {
    'quiz': fields.List(fields.Nested(quiz_question), description='Generated quiz questions')
})

error_response = ns.model('ErrorResponse', {
    'error': fields.String(description='Error message')
})

@ns.route('/generate')
class QuizResource(Resource):
    @ns.doc('generate_quiz')
    @ns.expect(quiz_request)
    @ns.response(200, 'Success', quiz_response)
    @ns.response(400, 'Validation Error', error_response)
    def post(self):
        """
        Generate a quiz from input text
        
        This endpoint accepts text content and returns a structured quiz based on that content.
        """
        data = request.get_json()
        input_text = data.get('text', '')

        # If no text is in the request body - return an error
        if not input_text:
            return {'error': 'No input text provided'}, 400

        # Generate quiz
        quiz = generate_quiz(input_text)

        # Return as json
        return {'quiz': quiz}

@ns.route('/document/<int:doc_id>')
@ns.param('doc_id', 'The document identifier')
class DocumentQuizResource(Resource):
    @ns.doc('generate_quiz_from_document')
    @ns.response(200, 'Success', quiz_response)
    @ns.response(404, 'Document not found', error_response)
    @ns.response(500, 'Internal Server Error', error_response)
    def get(self, doc_id):
        """
        Generate a quiz from a previously uploaded document
        
        This endpoint retrieves a document by ID and generates a quiz from its text content.
        """
        try:
            # Retrieve document from database
            document = Document.query.get(doc_id)
            
            if not document:
                return {'error': f'Document with ID {doc_id} not found'}, 404
            
            # Generate quiz from document content
            quiz = generate_quiz(document.content)
            
            return {'quiz': quiz}, 200
            
        except Exception as e:
            return {'error': f'Error generating quiz: {str(e)}'}, 500


def generate_quiz(text):
    """
    Takes extracted text and generates a structured quiz
    by calling OpenAI's Chat Completions API.
    """
    try:
        # Try with direct import (for newer versions of openai)
        import openai
        
        # Set API key
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Try newer client method
        try:
            client = openai.OpenAI(api_key=openai.api_key)
            
            # Send prompt to OpenAI and request a chat completion
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": create_prompt(text)}],
                temperature=0.7,
                max_tokens=500,
            )
            
            raw_quiz = response.choices[0].message.content  # extract text from OpenAI
            
        except (AttributeError, TypeError):
            # Fall back to older API style
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": create_prompt(text)}],
                temperature=0.7,
                max_tokens=500,
            )
            
            raw_quiz = response.choices[0].message.content  # extract text from OpenAI
            
        # Parse raw quiz text into JSON 
        return parse_quiz_to_json(raw_quiz)
        
    except Exception as e:
        # If all else fails, provide a sample quiz for testing
        return create_sample_quiz(text)


def create_prompt(text):
    """Create the prompt for OpenAI"""
    return f"""
    Generate a short 3-question multiple-choice quiz based on the following content:

    "{text}"

    Format:
    1. Question
       a) Option
       b) Option
       c) Option
       d) Option
       Answer: b)
    """


def parse_quiz_to_json(quiz_text):
    """
    Parses the OpenAI-generated quiz text into structured JSON:
    [
      {
        "question": "...",
        "options": [...],
        "answer": "..."
      },
      ...
    ]
    """
    # Split text into blocks based on questions
    questions = re.split(r'\n(?=\d+\.)', quiz_text.strip())
    structured = []

    for q in questions:
        lines = q.strip().split('\n')  # Split each block into lines
        if len(lines) < 6:
            continue  # Skip incomplete questions

        # Extract question text
        question_text = lines[0].split('.', 1)[1].strip() if len(lines[0].split('.', 1)) > 1 else "Question"

        # Extract options
        options = []
        for i in range(1, min(5, len(lines))):
            parts = lines[i].split(')', 1)
            if len(parts) > 1:
                options.append(parts[1].strip())
        
        if len(options) < 4:
            continue  # Skip if we don't have enough options

        # Extract the correct answer 
        answer_line = lines[-1]
        answer_letter = re.search(r'Answer:\s*([a-d])\)?', answer_line, re.IGNORECASE)
        if not answer_letter:
            continue  # Skip if no answer found

        # Map answer to the option
        answer_index = ord(answer_letter.group(1).lower()) - ord('a')
        if not (0 <= answer_index < len(options)):
            answer_index = 0  # Default to first option if index is out of range

        structured.append({
            "question": question_text,
            "options": options,
            "answer": options[answer_index]
        })

    return structured


def create_sample_quiz(text):
    """Create a sample quiz when OpenAI generation fails"""
    # Extract a few words to use in the sample quiz
    words = text.split()
    topic = " ".join(words[:3]) if len(words) >= 3 else "this topic"
    
    return [
        {
            "question": f"What is the main subject of the text about {topic}?",
            "options": [
                "The historical context", 
                "The key concepts", 
                "The practical applications", 
                "The future developments"
            ],
            "answer": "The key concepts"
        },
        {
            "question": "How would you best categorize this content?",
            "options": [
                "Instructional", 
                "Informative", 
                "Persuasive", 
                "Narrative"
            ],
            "answer": "Informative"
        },
        {
            "question": "What approach does the text primarily use?",
            "options": [
                "Chronological", 
                "Compare and contrast", 
                "Problem-solution", 
                "Descriptive"
            ],
            "answer": "Descriptive"
        }
    ]