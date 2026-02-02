import streamlit as st
from app import process_resume, generate_wordcloud
import matplotlib.pyplot as plt
# frontend.py

import streamlit as st
from app import process_resume, generate_wordcloud
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="EasyRecruitAI", layout="wide")

# Header
st.title("🚀 EasyRecruitAI")
st.subheader("AI Assistant for Job Matching & Resume Analysis")

# Sidebar: Role selection
role = st.sidebar.radio("Select Role", ["Job Seeker", "Job Recruiter"])

# File upload OR type skills manually
resume_text = st.text_area("Enter your skills (comma separated)", "Python, SQL, Machine Learning")

if st.button("Process Resume"):
    # Call backend function
    matched_jobs = process_resume(resume_text)
    st.write("### Matched Jobs:")
    st.write(matched_jobs)
    
    # Generate word cloud
    plt = generate_wordcloud(resume_text)
    st.pyplot(plt)