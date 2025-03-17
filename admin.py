import streamlit as st
import pandas as pd
from datetime import datetime

def show_admin_dashboard():
    # Check if user is authenticated first
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.title("Admin Authentication Required")
        st.warning("You need to be authenticated to access this dashboard.")
        
        with st.form("admin_login_form"):
            admin_password = st.text_input("Admin Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if admin_password == "admin":
                    st.session_state.admin_authenticated = True
                    st.success("Authentication successful!")
                    st.rerun()
                else:
                    st.error("Invalid password. Please try again.")
        
        # Add navigation back to main page
        if st.button("Back to Chat"):
            st.query_params.clear()
            st.rerun()
            
        return
    
    # If authenticated, show the dashboard
    st.title("TalentScout Admin Dashboard")

    # Add navigation in sidebar
    with st.sidebar:
        st.title("Navigation")
        if st.button("Back to Chat"):
            st.query_params.clear()
            st.rerun()
        if st.button("Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()

    # Get candidate data from session state
    if 'all_candidates' not in st.session_state:
        st.session_state.all_candidates = []

    candidates = st.session_state.all_candidates

    if not candidates:
        st.warning("No candidate data available yet.")
        return

    # Convert candidate data to DataFrame - use actual data since we're in admin view
    df = pd.DataFrame(candidates)

    # Sidebar filters
    st.sidebar.title("Filters")

    # Filter by position
    if 'position' in df.columns:
        positions = ['All'] + list(df['position'].unique())
        selected_position = st.sidebar.selectbox('Filter by Position', positions)
        if selected_position != 'All':
            df = df[df['position'] == selected_position]

    # Filter by experience with buffer for min/max values
    if 'experience' in df.columns:
        # Convert experience column to float
        df['experience'] = df['experience'].astype(float)

        min_exp = df['experience'].min()
        max_exp = df['experience'].max()

        # Add buffer if min equals max
        if min_exp == max_exp:
            min_exp = max(0.0, min_exp - 1.0)  # Ensure we don't go below 0
            max_exp = max_exp + 1.0

        exp_range = st.sidebar.slider(
            'Years of Experience',
            min_value=float(min_exp),
            max_value=float(max_exp),
            value=(float(min_exp), float(max_exp)),
            step=0.5  # Add step for more granular control
        )
        df = df[df['experience'].between(exp_range[0], exp_range[1])]

    # Main content area
    st.subheader("Candidate Overview")

    # Calculate overall score for each candidate
    def calculate_overall_score(row):
        score_sum = 0
        count = 0
        
        # Technical scores (multiple questions)
        if 'technical_analysis' in row and row['technical_analysis']:
            tech_scores = [qa['analysis']['score'] for qa in row['technical_analysis']]
            score_sum += sum(tech_scores)
            count += len(tech_scores)
        
        # Project experience score
        if 'project_analysis' in row and row['project_analysis'] and 'analysis' in row['project_analysis']:
            score_sum += row['project_analysis']['analysis']['score']
            count += 1
            
        # Problem solving score
        if 'problem_solving_analysis' in row and row['problem_solving_analysis'] and 'analysis' in row['problem_solving_analysis']:
            score_sum += row['problem_solving_analysis']['analysis']['score']
            count += 1
            
        # Learning approach score
        if 'learning_analysis' in row and row['learning_analysis'] and 'analysis' in row['learning_analysis']:
            score_sum += row['learning_analysis']['analysis']['score']
            count += 1
            
        # Calculate average if we have any scores
        if count > 0:
            return round(score_sum / count, 1)
        else:
            return "N/A"
    
    # Apply the calculation to each row
    overview_df = df[['name', 'email', 'position', 'experience', 'location']].copy()
    overview_df['Overall Score'] = df.apply(calculate_overall_score, axis=1)
    
    # Display the updated table
    st.dataframe(overview_df, use_container_width=True)

    # Detailed candidate view
    st.subheader("Detailed Candidate Information")
    selected_candidate = st.selectbox(
        "Select a candidate to view detailed information",
        df['name'].tolist()
    )

    if selected_candidate:
        candidate_data = df[df['name'] == selected_candidate].iloc[0]

        st.write("### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {candidate_data['name']}")
            st.write(f"**Email:** {candidate_data['email']}")
            st.write(f"**Phone:** {candidate_data['phone']}")
        with col2:
            st.write(f"**Position:** {candidate_data['position']}")
            st.write(f"**Experience:** {candidate_data['experience']} years")
            st.write(f"**Location:** {candidate_data['location']}")

        st.write("### Technical Background")
        st.write(f"**Tech Stack:** {candidate_data['tech_stack']}")

        # Technical Assessment Section
        if 'technical_analysis' in candidate_data:
            st.write("### Technical Assessment")

            # Display all questions first
            st.write("**Questions Asked:**")
            for i, qa in enumerate(candidate_data['technical_analysis'], 1):
                st.write(f"{i}. {qa['question']}")

            with st.expander("View Technical Assessment Response and Analysis"):
                # Display the combined response once
                st.write("**Combined Response:**")
                st.write(candidate_data['technical_analysis'][0]['answer'])

                # Calculate average score
                avg_score = sum(qa['analysis']['score'] for qa in candidate_data['technical_analysis']) / len(candidate_data['technical_analysis'])

                # Display metrics
                st.metric("Average Score", f"{avg_score:.1f}/10")

                # Aggregate strengths and improvements
                all_strengths = []
                all_improvements = []
                for qa in candidate_data['technical_analysis']:
                    all_strengths.extend(qa['analysis']['strengths'])
                    all_improvements.extend(qa['analysis']['improvements'])

                st.write("**Key Strengths:**")
                unique_strengths = list(set(all_strengths))
                for strength in unique_strengths:
                    st.write(f"✓ {strength}")

                st.write("**Areas for Improvement:**")
                unique_improvements = list(set(all_improvements))
                for improvement in unique_improvements:
                    st.write(f"○ {improvement}")

        # Project Experience Section
        if 'project_analysis' in candidate_data:
            st.write("### Project Experience")
            with st.expander("View Project Details and Analysis"):
                st.write("**Response:**")
                st.write(candidate_data['project_analysis']['details'])

                analysis = candidate_data['project_analysis']['analysis']
                st.metric("Score", f"{analysis['score']}/10")
                st.write("**Overall Assessment:**")
                st.write(analysis['overall_assessment'])

                st.write("**Key Strengths:**")
                for strength in analysis['strengths']:
                    st.write(f"✓ {strength}")

                st.write("**Areas for Improvement:**")
                for improvement in analysis['improvements']:
                    st.write(f"○ {improvement}")

        # Problem Solving Section
        if 'problem_solving_analysis' in candidate_data:
            st.write("### Problem Solving Approach")
            with st.expander("View Problem Solving Details and Analysis"):
                st.write("**Response:**")
                st.write(candidate_data['problem_solving_analysis']['details'])

                analysis = candidate_data['problem_solving_analysis']['analysis']
                st.metric("Score", f"{analysis['score']}/10")
                st.write("**Overall Assessment:**")
                st.write(analysis['overall_assessment'])

                st.write("**Key Strengths:**")
                for strength in analysis['strengths']:
                    st.write(f"✓ {strength}")

                st.write("**Areas for Improvement:**")
                for improvement in analysis['improvements']:
                    st.write(f"○ {improvement}")

        # Learning Approach Section
        if 'learning_analysis' in candidate_data:
            st.write("### Learning & Development")
            with st.expander("View Learning Approach Details and Analysis"):
                st.write("**Response:**")
                st.write(candidate_data['learning_analysis']['details'])

                analysis = candidate_data['learning_analysis']['analysis']
                st.metric("Score", f"{analysis['score']}/10")
                st.write("**Overall Assessment:**")
                st.write(analysis['overall_assessment'])

                st.write("**Key Strengths:**")
                for strength in analysis['strengths']:
                    st.write(f"✓ {strength}")

                st.write("**Areas for Improvement:**")
                for improvement in analysis['improvements']:
                    st.write(f"○ {improvement}")