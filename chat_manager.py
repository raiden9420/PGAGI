import streamlit as st
from gemini_helper import generate_technical_questions, analyze_response
from data_validator import validate_email, validate_phone

class ChatManager:
    def __init__(self):
        self.steps = {
            'bulk_input': self.handle_bulk_input,
            'technical_questions': self.handle_technical_questions,
            'project_details': self.handle_project_details,
            'problem_solving': self.handle_problem_solving,
            'learning_approach': self.handle_learning_approach,
            'farewell': self.handle_farewell
        }
        self.current_step = 'bulk_input'
        if 'all_candidates' not in st.session_state:
            st.session_state.all_candidates = []

    def process_input(self, user_input: str, current_step: str) -> str:
        """Process user input based on current conversation step"""
        handler = self.steps.get(current_step)
        if handler:
            return handler(user_input)
        return "I'm sorry, I didn't understand that. Could you please try again?"

    def get_next_step(self) -> str:
        """Return the current step after possible updates"""
        return self.current_step

    def handle_bulk_input(self, user_input: str) -> str:
        """Process initial bulk candidate information input"""
        try:
            data = [part.strip() for part in user_input.split(',')]
            if len(data) != 7:
                return ("Please provide all information in the correct format:\n"
                       "Name, Email, Phone, Years of Experience, Desired Position, Current Location, Tech Stack\n"
                       "Example: John Doe, john@example.com, +1-234-567-8900, 5, Software Engineer, New York, Python/Django/React")

            name, email, phone, experience, position, location, tech_stack = data

            if not validate_email(email):
                return "Please provide a valid email address."
            if not validate_phone(phone):
                return "Please provide a valid phone number."

            try:
                experience = float(experience)
            except ValueError:
                return "Please provide a valid number for years of experience."

            candidate_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'experience': experience,
                'position': position,
                'location': location,
                'tech_stack': tech_stack,
                'status': 'In Progress'
            }

            st.session_state.candidate_data = candidate_data
            self.current_step = 'technical_questions'
            questions = generate_technical_questions(tech_stack)
            # Format questions without adding numbering if they already start with numbers
            formatted_questions = []
            for i, q in enumerate(questions):
                # Check if the question already starts with a number pattern (like "1." or "1)")
                if q.strip().startswith(("1.", "2.", "3.", "4.", "5.")):
                    formatted_questions.append(q)
                else:
                    formatted_questions.append(f"{i+1}. {q}")

            return (f"Thank you, {name.split()[0]}! I can see you're interested in the {position} role "
                   f"with {experience} years of experience. Based on your tech stack ({tech_stack}), "
                   "I'd like to ask you a few technical questions:\n\n" +
                   "\n".join(formatted_questions))

        except Exception as e:
            return ("I couldn't process your input. Please ensure it's in the correct format:\n"
                   "Name, Email, Phone, Years of Experience, Desired Position, Current Location, Tech Stack")

    def handle_technical_questions(self, user_input: str) -> str:
        """Process candidate's technical responses"""
        questions = generate_technical_questions(st.session_state.candidate_data['tech_stack'])
        analysis_results = []
        for i, question in enumerate(questions):
            analysis = analyze_response(question, user_input)
            analysis_results.append({
                'question': question,
                'answer': user_input,
                'analysis': analysis
            })
        st.session_state.candidate_data['technical_analysis'] = analysis_results
        self.current_step = 'project_details'
        return (f"Thanks for those insights! Your experience with {st.session_state.candidate_data['tech_stack']} sounds interesting. "
                "Could you tell me more about your most challenging or impactful project? "
                "Please include:\n"
                "• The problem you were solving\n"
                "• Technologies you used\n"
                "• Your specific role\n"
                "• The outcome and its impact")

    def handle_project_details(self, user_input: str) -> str:
        """Process candidate's project experience details"""
        analysis = analyze_response("Describe your most challenging or impactful project", user_input)
        st.session_state.candidate_data['project_analysis'] = {
            'details': user_input,
            'analysis': analysis
        }
        self.current_step = 'problem_solving'
        return ("That's a fascinating project! Now, could you share a specific technical challenge you encountered during development? "
                "How did you approach solving it? What alternatives did you consider?")

    def handle_problem_solving(self, user_input: str) -> str:
        """Process candidate's problem-solving approach"""
        analysis = analyze_response("Describe a technical challenge and your problem-solving approach", user_input)
        st.session_state.candidate_data['problem_solving_analysis'] = {
            'details': user_input,
            'analysis': analysis
        }
        self.current_step = 'learning_approach'
        return ("Your problem-solving approach is interesting! One last question: "
                "How do you stay updated with the latest developments in your field? "
                "Could you share any specific resources you use or any recent technology/concept you've learned?")

    def handle_learning_approach(self, user_input: str) -> str:
        """Process candidate's learning and development approach"""
        analysis = analyze_response("How do you stay updated with the latest developments in your field?", user_input)
        st.session_state.candidate_data['learning_analysis'] = {
            'details': user_input,
            'analysis': analysis
        }
        st.session_state.candidate_data['status'] = 'Completed'
        if 'all_candidates' not in st.session_state:
            st.session_state.all_candidates = []
        # Store original data for admin view
        st.session_state.all_candidates.append(st.session_state.candidate_data.copy())
        self.current_step = 'farewell'
        return (f"Thank you for sharing your experience and insights, {st.session_state.candidate_data['name'].split()[0]}! "
                "I've collected comprehensive information about your:\n"
                "• Technical expertise and experience\n"
                "• Project implementation skills\n"
                "• Problem-solving approach\n"
                "• Continuous learning mindset\n\n"
                "Our hiring team will carefully review your responses and contact you via email about the next steps. "
                "Would you like to end the conversation? (You can type 'exit' to finish)")

    def handle_farewell(self, user_input: str) -> str:
        """Handle the farewell message"""
        if 'candidate_data' in st.session_state and 'name' in st.session_state.candidate_data:
            name = st.session_state.candidate_data['name'].split()[0]
        else:
            name = "candidate"

        return (f"Thank you for your time, {name}! "
                "We appreciate your detailed responses and interest in joining our team. "
                "You'll hear from us soon via email. Have a great day!")

    def end_conversation(self) -> str:
        """End the conversation and return a farewell message"""
        self.current_step = 'farewell'
        if 'candidate_data' in st.session_state and st.session_state.candidate_data and 'name' in st.session_state.candidate_data:
            name = st.session_state.candidate_data['name'].split()[0]
            return f"Thank you for your time, {name}! Have a great day!"
        return "Thank you for your time! Have a great day!"