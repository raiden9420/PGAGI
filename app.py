
import streamlit as st
from chat_manager import ChatManager
from data_validator import validate_email, validate_phone
from admin import show_admin_dashboard

def initialize_session_state():
    if 'chat_manager' not in st.session_state:
        st.session_state.chat_manager = ChatManager()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Add initial message
        st.session_state.messages.append({
            "role": "assistant",
            "content": ("Welcome to TalentScout! I'm your hiring assistant. Please provide your information in the following format:\n"
                       "Name, Email, Phone, Years of Experience, Desired Position, Current Location, Tech Stack\n"
                       "Example: John Doe, john@example.com, +1-234-567-8900, 5, Software Engineer, New York, Python/Django/React")
        })
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'bulk_input'
    if 'candidate_data' not in st.session_state:
        st.session_state.candidate_data = {}
    if 'all_candidates' not in st.session_state:
        st.session_state.all_candidates = []
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False

def main():
    # Check if admin route is requested
    if st.query_params.get("route", "") == "admin":
        show_admin_dashboard()
        return

    st.title("TalentScout Hiring Assistant")
    st.markdown("*An intelligent recruiting assistant for technical positions*")
    
    # Add instructions in an expandable section
    with st.expander("📋 How to Use TalentScout", expanded=True):
        st.markdown("""
        ### Instructions for Candidates:
        
        1. **Getting Started**: 
           * Enter your information in the format requested (Name, Email, Phone, etc.)
           * Be specific about your tech stack (e.g., Python/Django/React, Java/Spring/Angular)
        
        2. **Technical Assessment**:
           * The AI will generate questions specific to your tech stack
           * Answer all questions in detail to showcase your expertise
        
        3. **Project Experience**:
           * Describe your most significant project with clear details about your role
           * Highlight technologies used and challenges overcome
        
        4. **Problem-Solving**:
           * Explain your approach to solving technical problems
           * Include specific examples where possible
        
        5. **Tips for Best Results**:
           * Be concise but thorough in your responses
           * Type 'exit' or 'quit' anytime to end the conversation
           * Administrative staff can access the dashboard via the sidebar
        
        The AI assistant will guide you through each step of the process.
        """)
        
    # Add a visual separator
    st.markdown("---")

    initialize_session_state()
    
    # Add admin access in sidebar
    with st.sidebar:
        st.title("Navigation")
        
        # Admin authentication section
        with st.expander("Admin Access", expanded=False):
            if not st.session_state.admin_authenticated:
                admin_password = st.text_input("Admin Password", type="password")
                if st.button("Login"):
                    # For demo purposes, use a simple password
                    # In production, use a more secure approach
                    if admin_password == "admin":
                        st.session_state.admin_authenticated = True
                        st.success("Authentication successful!")
                        st.rerun()
                    else:
                        st.error("Invalid password")
            else:
                st.success("Admin authenticated")
                if st.button("Access Admin Dashboard"):
                    st.query_params["route"] = "admin"
                    st.rerun()
                if st.button("Logout"):
                    st.session_state.admin_authenticated = False
                    st.rerun()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user input
    if user_input := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Process user input based on current step
        chat_manager = st.session_state.chat_manager

        if user_input.lower() in ['exit', 'quit', 'bye']:
            response = chat_manager.end_conversation()
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

        response = chat_manager.process_input(user_input, st.session_state.current_step)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Update current step if needed
        new_step = chat_manager.get_next_step()
        if new_step != st.session_state.current_step:
            st.session_state.current_step = new_step

        st.rerun()

if __name__ == "__main__":
    main()
