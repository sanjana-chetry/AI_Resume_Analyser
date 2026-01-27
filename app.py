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
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    return "File uploaded successfully!"   # Temporary response
if __name__ == "__main__":
    app.run(debug=True)
