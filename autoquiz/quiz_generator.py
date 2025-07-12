import openai
import os
import re

# Load OpenAI API key 
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_quiz(text):
    """
    Takes extracted text and generates a structured quiz
    by calling OpenAI's Chat Completions API.
    """
    client = openai.OpenAI()  # Initialize client

    # Prompt on how to generate a quiz
    prompt = f"""
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

    # Send prompt to OpenAI and request a chat completion
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
    )

    raw_quiz = response.choices[0].message.content  # extract text from OpenAI

    # Parse raw quiz text into JSON 
    return parse_quiz_to_json(raw_quiz)

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
        question_text = lines[0].split('.', 1)[1].strip()

        # Extract options
        options = [line.split(')', 1)[1].strip() for line in lines[1:5]]

        # Extract the correct answer 
        answer_line = lines[-1]
        answer_letter = re.search(r'Answer:\s*([a-d])\)?', answer_line, re.IGNORECASE)
        if not answer_letter:
            continue  # Skip if no answer found

        # Map answer to the option
        answer_index = ord(answer_letter.group(1).lower()) - ord('a')

        structured.append({
            "question": question_text,
            "options": options,
            "answer": options[answer_index] if 0 <= answer_index < len(options) else None
        })

    return structured
