import os
from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from google import genai
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is missing! Please check your .env file")

app = Flask(__name__)

# Initialize Gemini client
client = genai.Client(api_key=gemini_api_key)

# Extract text from uploaded PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# Analyze resume vs job description
def analyze_resume(resume_text, job_desc):
    prompt_text = f"""
You are an AI career assistant.
A candidate submitted this resume:
{resume_text}

The job description is:
{job_desc}

Task:
1. Provide resume improvement suggestions.
2. Generate exactly 10 interview questions.

Important:
Return ONLY JSON in this exact format:
{{
  "analysis": "string with suggestions",
  "interview_questions": ["Question1", "Question2", ..., "Question10"]
}}
Do not include any extra text, explanations, or markdown.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text
        )
        content = response.text.strip()

        # Extract JSON safely even if extra text exists
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            json_str = match.group()
            result = json.loads(json_str)
        else:
            # fallback: return raw text
            result = {"analysis": content, "interview_questions": []}

    except Exception as e:
        result = {
            "analysis": f"Error generating analysis: {str(e)}",
            "interview_questions": []
        }

    return result

# API endpoint
@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    file = request.files["resume"]
    job_desc = request.form.get("job_description", "")

    if not job_desc:
        return jsonify({"error": "No job description provided"}), 400

    # Save resume
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", "temp_resume.pdf")
    file.save(file_path)

    # Extract text and analyze
    resume_text = extract_text_from_pdf(file_path)
    result = analyze_resume(resume_text, job_desc)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
