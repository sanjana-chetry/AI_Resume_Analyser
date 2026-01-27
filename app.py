from flask import Flask, render_template,request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["resume"]         # Receive file from form

    if file.filename == "":
        return "No file selected"

    # Save file in uploads folder
    
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return render_template("index.html", message="File uploaded successfully!") #response
  
if __name__ == "__main__":
    app.run(debug=True)
