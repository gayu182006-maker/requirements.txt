import streamlit as st
import pdfplumber
import docx2txt
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
from fpdf import FPDF
import io

# ---------------- STEP 1: ROLE SELECTION ----------------
st.sidebar.title("User Role")
role = st.sidebar.radio(
    "Select your role",
    ["Job Seeker", "HR / Interviewer"],
    key="role_selector"
)

st.title("🚀 Smart Resume & Interview Assistant")
st.write(f"Selected Role: **{role}**")

# ---------------- STEP 2: RESUME UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF / DOCX)",
    type=["pdf", "docx"],
    key="resume_upload"
)

# ---------------- TEXT EXTRACTION ----------------
def extract_text(file):
    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    else:
        return docx2txt.process(file)

# ---------------- RESUME ANALYSIS ----------------
def analyze_resume(text):
    skills = ["python", "sql", "machine learning", "java", "excel"]
    text = text.lower()
    found = [s for s in skills if s in text]
    missing = [s for s in skills if s not in found]
    score = int((len(found)/len(skills))*100)
    return found, missing, score

# ---------------- JOB POSITIONS ----------------
job_positions = {
    "Data Analyst": ["python", "sql", "excel"],
    "Machine Learning Engineer": ["python", "machine learning", "sql"],
    "Java Developer": ["java", "sql"],
    "Business Analyst": ["excel", "sql"]
}

# ---------------- PROCESS RESUME ----------------
if uploaded_file:
    resume_text = extract_text(uploaded_file)
    found, missing, score = analyze_resume(resume_text)

    st.success("✅ Resume analyzed successfully!")

    # ---------------- JOB RECOMMENDATION ----------------
    matched_jobs = []
    for job, skills_required in job_positions.items():
        match_count = len([s for s in skills_required if s in found])
        if match_count > 0:
            matched_jobs.append((job, match_count))
    matched_jobs.sort(key=lambda x: x[1], reverse=True)

    # ---------------- COMMON GRAPHS & WORDCLOUD ----------------
    # Pie chart for skills
    labels = ['Matched Skills', 'Missing Skills']
    sizes = [len(found), len(missing)]
    colors = ['green','red']
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax1.axis('equal')

    # WordCloud
    wordcloud = WordCloud(width=400, height=200, background_color='white').generate(resume_text)
    
    # Keyword frequency
    words = re.findall(r'\w+', resume_text.lower())
    word_counts = Counter(words)
    most_common = word_counts.most_common(10)

    # ---------------- JOB SEEKER DASHBOARD ----------------
    if role == "Job Seeker":
        st.header("👤 Job Seeker Dashboard")
        st.metric("Resume Score", f"{score}%")
        st.subheader("Your Skills")
        st.write(found)
        st.subheader("Skills to Improve")
        st.write(missing)

        st.subheader("📊 Skills Overview Pie Chart")
        st.pyplot(fig1)

        st.subheader("Resume Keywords WordCloud")
        plt.figure(figsize=(8,4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

        st.subheader("🔑 Top 10 Keywords in Resume")
        plt.figure(figsize=(8,4))
        plt.bar([x[0] for x in most_common], [x[1] for x in most_common], color='purple')
        plt.ylabel("Frequency")
        plt.xticks(rotation=45)
        st.pyplot(plt)

        st.subheader("💼 Recommended Jobs")
        for job, count in matched_jobs:
            st.write(f"{job} — {count} skills matched")

        # Download PDF
        if st.button("📄 Download Resume Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200,10,txt="Resume Analysis Report", ln=True, align='C')
            pdf.ln(10)
            pdf.cell(200,10,txt=f"Resume Score: {score}%", ln=True)
            pdf.ln(5)
            pdf.cell(200,10,txt=f"Matched Skills: {', '.join(found)}", ln=True)
            pdf.ln(5)
            pdf.cell(200,10,txt=f"Missing Skills: {', '.join(missing)}", ln=True)
            pdf.ln(5)
            pdf.cell(200,10,txt=f"Recommended Jobs: {', '.join([job for job,_ in matched_jobs])}", ln=True)
            pdf_output = io.BytesIO()
            pdf.output(pdf_output)
            pdf_output.seek(0)
            st.download_button("Download PDF", data=pdf_output, file_name="resume_analysis.pdf", mime="application/pdf")

    # ---------------- HR DASHBOARD ----------------
    if role == "HR / Interviewer":
        st.header("👨‍💼 HR / Interviewer Dashboard")
        st.metric("Candidate Suitability", f"{score}%")
        st.subheader("Candidate Strengths")
        st.write(found)
        st.subheader("Skill Gaps")
        st.write(missing)

        st.subheader("Suggested Interview Questions")
        for skill in found:
            st.write(f"• Ask advanced questions on {skill}")

        st.subheader("Interview Evaluation")
        rating = st.slider("Rate Candidate", 1, 10, key="rating_slider")
        if st.button("Finalize Decision", key="finalize_button"):
            if rating >= 7:
                st.success("✅ SELECT")
            elif rating >= 5:
                st.warning("⏳ HOLD")
            else:
                st.error("❌ REJECT")

        st.subheader("📊 Skills Overview Pie Chart")
        st.pyplot(fig1)

        st.subheader("Resume Keywords WordCloud")
        plt.figure(figsize=(8,4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

        st.subheader("🔑 Top 10 Keywords in Resume")
        plt.figure(figsize=(8,4))
        plt.bar([x[0] for x in most_common], [x[1] for x in most_common], color='purple')
        plt.ylabel("Frequency")
        plt.xticks(rotation=45)
        st.pyplot(plt)

        st.subheader("💼 Recommended Jobs for Candidate")
        for job, count in matched_jobs:
            st.write(f"{job} — {count} skills matched")

        # Download PDF
        if st.button("📄 Download Candidate Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200,10,txt="Candidate Resume Report", ln=True, align='C')
            pdf.ln(10)
            pdf.cell(200,10,txt=f"Resume Score: {score}%", ln=True)
            pdf.ln(5)
            pdf.cell(200,10,txt=f"Candidate Strengths: {', '.join(found)}", ln=True)
            pdf.ln(5)
            pdf.cell(200,10,txt=f"Skill Gaps: {', '.join(missing)}", ln=True)
            pdf.ln(5)
            pdf.cell(200,10,txt=f"Recommended Jobs: {', '.join([job for job,_ in matched_jobs])}", ln=True)
            pdf_output = io.BytesIO()
            pdf.output(pdf_output)
            pdf_output.seek(0)
            st.download_button("Download PDF", data=pdf_output, file_name="candidate_analysis.pdf", mime="application/pdf")