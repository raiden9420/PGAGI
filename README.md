# TalentScout - AI-Powered Hiring Assistant

## Project Overview
TalentScout is an intelligent chatbot that streamlines the technical hiring process. It conducts interactive interviews, assesses candidates' technical skills, and provides detailed analytics for hiring managers. The assistant adapts its questions based on candidates' tech stacks and provides comprehensive evaluations of their responses.

## Installation Instructions

1. Clone or download the project
2. Install required packages:
```bash
pip install streamlit google-generativeai pandas python-dotenv
```
3. Get a Gemini API key from [Google MakerSuite](https://makersuite.google.com/app/apikey)
4. Create a `.env` file in the root directory:
```
GOOGLE_API_KEY=your_api_key_here
```
5. Run the application:
```bash
streamlit run attached_assets/app.py
```
The app will be accessible at http://0.0.0.0:5000

## Usage Guide

### For Candidates
1. Enter your information in the requested format
2. Answer technical questions specific to your tech stack
3. Describe your projects and experience
4. Receive immediate feedback and evaluation

### For Administrators
1. Access admin dashboard via sidebar
2. Use password: "admin"
3. View candidate analytics and responses
4. Filter and sort candidates

## Technical Details

### Architecture
- Frontend: Streamlit
- AI Integration: Google Gemini AI
- Data Management: Session-based storage

### Key Components
1. `app.py`: Main application entry point and UI
2. `chat_manager.py`: Conversation flow management
3. `gemini_helper.py`: AI integration and prompt engineering
4. `admin.py`: Admin dashboard and analytics
5. `data_validator.py`: Input validation

## Prompt Design

The application uses carefully crafted prompts for:
1. Technical question generation based on tech stack
2. Response analysis for technical accuracy
3. Natural conversation flow
4. Comprehensive candidate assessment

### Example Prompt Structure
```python
system_prompt = "You are an expert technical interviewer..."
user_prompt = f"Given the tech stack: {tech_stack}, generate relevant questions..."
```

## Challenges & Solutions

1. **API Rate Limiting**
   - Challenge: Gemini API rate limits during high usage
   - Solution: Implemented exponential backoff and fallback questions

2. **Response Analysis**
   - Challenge: Maintaining consistent evaluation criteria
   - Solution: Structured JSON response format with specific scoring metrics

3. **Conversation Flow**
   - Challenge: Natural progression through interview stages
   - Solution: State management system with defined conversation steps

4. **Data Persistence**
   - Challenge: Maintaining session data
   - Solution: Streamlit session state management with structured data storage


## Best Practices

- Modular code structure for maintainability
- Comprehensive error handling
- Clear code documentation
- Secure authentication implementation
- Responsive UI design

## Contributing

This project is part of an assignment implementation. For any suggestions or improvements, please create an issue or contact the development team.

## License

This project is created as part of an AI/ML Intern assignment and is for demonstration purposes.