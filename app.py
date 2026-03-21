from flask import Flask, render_template, request
import os
import requests
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from utils.resume_parser import extract_text
from utils.text_cleaner import clean_text
from utils.skill_matcher import detect_skills
from utils.section_detector import detect_sections
from utils.ai_suggestions import get_suggestions

load_dotenv()

API_KEY = os.getenv("RESUME_VALIDATION_API_KEY")
VALIDATION_API_URL = os.getenv("RESUME_VALIDATION_API_URL")

# Fail immediately at startup if .env is missing critical keys
if not API_KEY or not VALIDATION_API_URL:
    raise EnvironmentError(
        "Missing RESUME_VALIDATION_API_KEY or RESUME_VALIDATION_API_URL in .env file."
    )

app = Flask(__name__)

# Secret key for Flask session security
app.secret_key = os.getenv("SECRET_KEY", "dev-fallback-key-change-in-production")

# Max upload size: 2MB
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


# Error Handlers 

@app.errorhandler(404)
def page_not_found(e):
    return render_template("index.html", message="Page not found."), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("index.html", message="Something went wrong. Please try again."), 500


@app.errorhandler(413)
def file_too_large(e):
    return render_template("index.html", message="File too large. Maximum size is 2MB."), 413


# Routes

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():

    file = request.files.get("resume")

    # 1. Check a file was actually attached
    if not file or file.filename == "":
        return render_template("index.html", message="No file selected.")

    # 2. Validate file extension before saving anything
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return render_template(
            "index.html",
            message="Invalid file type. Please upload a PDF or DOCX."
        )

    # 3. Check role was selected
    selected_role = request.form.get("role")
    if not selected_role:
        return render_template("index.html", message="Please select a target role.")

    # 4. Save file safely (secure_filename prevents path traversal attacks)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    safe_name = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, safe_name)
    file.save(file_path)

    try:
        # 5. Validate resume via external API
        try:
            with open(file_path, "rb") as f:
                validation_response = requests.post(
                    VALIDATION_API_URL,
                    headers={"x-api-key": API_KEY},
                    files={"file": f},
                    timeout=15
                )
            validation_data = validation_response.json()

        except Exception:
            return render_template(
                "index.html",
                message="Validation service is unavailable. Please try again."
            )

        if validation_data.get("status") != "VALID_RESUME":
            return render_template(
                "index.html",
                message="Uploaded file does not appear to be a resume. Please upload a valid resume."
            )

        # 6. Extract text from the resume file
        try:
            text = extract_text(file_path)
        except (ValueError, RuntimeError) as e:
            return render_template("index.html", message=str(e))

        # 7. Reject if too little text was extracted (e.g. scanned image PDF)
        if len(text.strip()) < 50:
            return render_template(
                "index.html",
                message="Could not read enough text from your resume. Please upload a text-based PDF."
            )

        # 8. Clean text and run skill detection
        cleaned_text = clean_text(text)
        result = detect_skills(cleaned_text, selected_role)

        if "error" in result:
            return render_template("index.html", message=result["error"])

        # 9. Detect which resume sections are present
        sections = detect_sections(text)

        # 10. Get AI suggestions for missing skills
        suggestions = get_suggestions(result["missing_skills"])

    finally:
        # Always delete the uploaded file — runs even if an error occurred above
        if os.path.exists(file_path):
            os.remove(file_path)

    return render_template(
        "result.html",
        role=selected_role,
        matched=result["matched_skills"],
        missing=result["missing_skills"],
        score=result["match_score"],
        sections=sections,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(debug=False)
