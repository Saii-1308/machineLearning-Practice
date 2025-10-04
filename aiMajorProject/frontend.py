import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.title("AI Resume Analyzer & Interview Question Generator")

st.write("Upload your resume (PDF format) to get started:")

resume_file = st.file_uploader("Choose a file...", type="pdf")
job_description = st.text_area("Enter the job description:", height=150)

# Ensure uploads folder exists
os.makedirs("uploads", exist_ok=True)

if st.button("Analyze your resume"):
    if not resume_file:
        st.warning("Please upload your resume file")
    elif not job_description:
        st.warning("Please enter a job description")
    else:
        # Save uploaded resume
        resume_path = os.path.join("uploads", "temp_resume.pdf")
        with open(resume_path, "wb") as f:
            f.write(resume_file.getbuffer())

        # Send request to backend
        with st.spinner("Analyzing your resume..."):
            files = {"resume": open(resume_path, "rb")}
            data = {"job_description": job_description}

            try:
                response = requests.post("http://127.0.0.1:5001/analyze", files=files, data=data)
                result = response.json()

                # Display results
                st.subheader("📊 Resume Analysis")
                st.write(result.get("analysis", "No analysis received."))

                st.subheader("🎯 Top 10 Interview Questions")
                questions = result.get("interview_questions", [])
                if questions:
                    for i, q in enumerate(questions, 1):
                        st.markdown(f"**{i}.** {q}")
                else:
                    st.info("No interview questions generated.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
