from flask import Flask, render_template,request
import os
from utils.resume_parser import extract_text
from utils.text_cleaner import clean_text
from utils.skill_matcher import analyse_skills



app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("resume")
       # Receive file from form

    if file.filename == "":
        return "No file selected"

    # Save file in uploads folder
    
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    text = extract_text(file_path)
    cleaned_text = clean_text(text)

    #skill matcher
    selected_role=request.form.get("role")
    if not selected_role:
        return render_template("index.html", message="Please select a role")

    coverage,matched,missing=analyse_skills(cleaned_text,selected_role)

    return render_template(
        "result.html",
        role=selected_role,
        coverage=coverage,
        matched=matched,
        missing=missing
    )

    #print(matched)

    #print(cleaned_text[:])

    #print(text[:])   # print first 500 chars


   # return render_template("index.html", message="File uploaded successfully!") #response



  
if __name__ == "__main__":
    app.run(debug=True)
