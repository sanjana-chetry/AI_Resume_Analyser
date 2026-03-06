from flask import Flask, render_template, request
import os
import requests
from dotenv import load_dotenv
from utils.resume_parser import extract_text
from utils.text_cleaner import clean_text
from utils.skill_matcher import detect_skills

load_dotenv()

API_KEY = os.getenv("RESUME_VALIDATION_API_KEY")
VALIDATION_API_URL = os.getenv("RESUME_VALIDATION_API_URL")

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():

    file = request.files.get("resume")

    if not file or file.filename == "":
        return render_template("index.html", message="No file selected")

    # Save file
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Validate Resume
    try:
        with open(file_path, "rb") as f:
            validation_response = requests.post(
                VALIDATION_API_URL,
                headers={
                    "x-api-key": API_KEY
                },
                files={
                    "file": f
                },
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
            message="Uploaded file is not a valid resume."
        )

    # If valid-->extract & detect
    text = extract_text(file_path)
    cleaned_text = clean_text(text)

    selected_role = request.form.get("role")
    if not selected_role:
        return render_template("index.html", message="Please select a role")

    result = detect_skills(cleaned_text, selected_role)

    return render_template(
        "result.html",
        role=selected_role,
        matched=result["matched_skills"],
        missing=result["missing_skills"]
    )


if __name__ == "__main__":
    app.run(debug=True)