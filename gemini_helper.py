import os
import json
import time
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, InternalServerError, ServiceUnavailable

# Use Gemini API
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Configure the model
model = genai.GenerativeModel('gemini-1.5-flash')

MAX_RETRIES = 3
BASE_DELAY = 1

def analyze_response(question: str, answer: str) -> dict:
    """
    Analyze a candidate's response using Gemini.
    Returns a dict with score, strengths, and improvements.
    """
    for attempt in range(MAX_RETRIES):
        try:
            system_prompt = "You are an expert technical interviewer with extensive experience in evaluating candidate responses."
            
            user_prompt = f"""Analyze the following technical interview response:

Question: {question}
Answer: {answer}

Provide analysis in the following JSON format:
{{
    "score": <number between 0-10>,
    "strengths": [<list of key strengths>],
    "improvements": [<list of areas for improvement>],
    "overall_assessment": <brief overall evaluation>
}}

Focus on:
1. Technical accuracy
2. Communication clarity
3. Problem-solving approach
4. Practical experience
5. Understanding of concepts

Remember to respond only with valid JSON."""

            response = model.generate_content(
                [system_prompt, user_prompt],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                    response_mime_type="application/json"
                )
            )

            try:
                # The text attribute contains the response text
                result = json.loads(response.text)
                return result
            except json.JSONDecodeError:
                print("Invalid JSON response from Gemini during analysis")
                return generate_fallback_analysis()

        except ResourceExhausted as e:
            if attempt < MAX_RETRIES - 1:
                delay = BASE_DELAY * (2 ** attempt)
                time.sleep(delay)
                continue
            print(f"Rate limit reached during analysis: {str(e)}")
            return generate_fallback_analysis()

        except (InternalServerError, ServiceUnavailable, Exception) as e:
            print(f"API error during analysis: {str(e)}")
            return generate_fallback_analysis()

    return generate_fallback_analysis()

def generate_fallback_analysis() -> dict:
    """
    Generate a basic analysis when API calls fail.
    """
    return {
        "score": 5,
        "strengths": ["Response provided", "Attempted to address the question"],
        "improvements": ["Unable to perform detailed analysis"],
        "overall_assessment": "Analysis unavailable - manual review recommended"
    }

def generate_technical_questions(tech_stack: str) -> list:
    """
    Primary question generation using Gemini API.
    Only falls back to pre-defined questions if API fails.
    """
    for attempt in range(MAX_RETRIES):
        try:
            # System prompt to set the context
            system_prompt = "You are an expert technical interviewer specialized in software development and technology assessment."
            
            # Dynamic prompt based on provided tech stack
            user_prompt = f"""Given the following tech stack: {tech_stack}

Please generate 3-5 technical interview questions that:
1. Are specific to the mentioned technologies
2. Range from intermediate to advanced difficulty
3. Focus on practical application and problem-solving
4. Include a mix of conceptual and hands-on questions

Return the questions in this JSON format:
{{
    "questions": [
        "Question 1",
        "Question 2",
        "Question 3"
    ]
}}

Remember to respond only with valid JSON."""

            response = model.generate_content(
                [system_prompt, user_prompt],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=500,
                    response_mime_type="application/json"
                )
            )

            # Parse the response
            try:
                result = json.loads(response.text)
                if "questions" in result and isinstance(result["questions"], list):
                    return result["questions"][:5]
            except json.JSONDecodeError:
                print("Invalid JSON response from Gemini, using fallback questions")
                return generate_fallback_questions(tech_stack)

        except ResourceExhausted as e:
            if attempt < MAX_RETRIES - 1:
                delay = BASE_DELAY * (2 ** attempt)  # Exponential backoff
                time.sleep(delay)
                continue
            print(f"Rate limit reached after {MAX_RETRIES} attempts, using fallback questions")
            return generate_fallback_questions(tech_stack)

        except (InternalServerError, ServiceUnavailable, Exception) as e:
            print(f"API error: {str(e)}, using fallback questions")
            return generate_fallback_questions(tech_stack)

    return generate_fallback_questions(tech_stack)

def generate_fallback_questions(tech_stack: str) -> list:
    """
    Fallback question generation when API fails.
    Provides pre-defined questions based on tech stack.
    """
    # Extract technologies from the stack
    techs = [t.strip().lower() for t in tech_stack.split('/')]
    questions = []

    # Add a general project question using the first technology
    questions.append(f"Describe a challenging project you built using {techs[0]}.")

    # Add technology-specific questions
    for tech in techs:
        if 'python' in tech:
            questions.extend([
                "How do you handle dependency management in Python projects?",
                "What's your approach to Python testing and test automation?"
            ])
        elif 'javascript' in tech:
            questions.extend([
                "How do you handle asynchronous operations in JavaScript?",
                "Explain your experience with modern JavaScript frameworks."
            ])
        elif 'data' in tech or 'ml' in tech or 'ai' in tech:
            questions.extend([
                "How do you approach data preprocessing and feature engineering?",
                "What machine learning algorithms have you worked with?"
            ])
        elif 'web' in tech:
            questions.extend([
                "How do you ensure web application security?",
                "What's your approach to responsive design?"
            ])

    # Add general engineering questions if we need more
    general_questions = [
        "How do you approach debugging complex technical issues?",
        "Describe your experience with version control and collaboration.",
        "How do you stay updated with new technologies?",
        "What's your approach to code quality and maintainability?",
        "How do you handle technical debt in your projects?"
    ]

    # Combine questions and ensure we have exactly 5
    while len(questions) < 5:
        questions.append(general_questions[len(questions) - 5])

    return questions[:5]  # Return exactly 5 questions
