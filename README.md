# zCV — AI Resume Analyser

> AI-powered resume analyser that matches your skills to a job role and gives improvement suggestions. Built with Python, Flask, and Groq API.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## What it does

Upload your resume, select a target job role, and zCV will:

- Extract and analyse your resume text
- Match your skills against role-specific requirements
- Calculate an **ATS match score** (0–100%)
- Detect which resume sections are present
- Generate **AI-powered improvement suggestions** for missing skills

---

## Preview

| Dark Mode | Light Mode |
|-----------|------------|
| Upload your resume and select a role | Clean light theme with gradient background |

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, Vanilla JS, Jinja2 |
| File Parsing | pdfplumber, python-docx |
| AI Suggestions | Groq API (llama3-8b-8192) |
| Validation | External Resume Validation API |

---

## Features

- ✅ PDF and DOCX support
- ✅ Skill matching with synonym detection (e.g. `js` → `javascript`)
- ✅ Regex word-boundary matching (fixes `java` matching inside `javascript`)
- ✅ ATS match score with circular progress ring
- ✅ Resume section detection (Education, Experience, Skills, Projects, etc.)
- ✅ AI improvement suggestions per missing skill
- ✅ Dark / Light theme toggle
- ✅ Welcome animation on page load
- ✅ Drag and drop file upload
- ✅ Fully responsive — mobile, tablet, desktop
- ✅ Resumes never stored — deleted immediately after processing

---

## Supported Roles

Software Developer, Frontend Developer, Backend Developer, Full Stack Developer, Machine Learning Engineer, Data Scientist, AI Engineer, DevOps Engineer, Cybersecurity Engineer, Data Engineer, Android Developer, iOS Developer

---

## Project Structure

```
AI_Resume_Analyser/
├── app.py                     # Main Flask app
├── requirements.txt           # Python dependencies
├── .env                       # API keys (never commit this)
├── .gitignore
├── README.md
├── utils/
│   ├── resume_parser.py       # Extracts text from PDF/DOCX
│   ├── text_cleaner.py        # Cleans extracted text
│   ├── skill_matcher.py       # Matches skills against role
│   ├── section_detector.py    # Detects resume sections
│   ├── ai_suggestions.py      # Groq API suggestions
│   └── role_skills.json       # Skill data per role
├── templates/
│   ├── index.html             # Upload page
│   └── result.html            # Results page
└── static/
    ├── style.css              # Index page styles
    ├── result.css             # Result page styles
    ├── script.js              # Frontend interactions
    └── favicon.png
```

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/AI_Resume_Analyser.git
cd AI_Resume_Analyser
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your `.env` file
Create a `.env` file in the root folder:
```
RESUME_VALIDATION_API_KEY=your_key_here
RESUME_VALIDATION_API_URL=your_url_here
GROQ_API_KEY=your_groq_key_here
SECRET_KEY=any-random-string-here
```

> Get a free Groq API key at [console.groq.com](https://console.groq.com)
> `GROQ_API_KEY` is optional — if not set, AI suggestions are skipped silently

### 5. Run the app
```bash
python app.py
```

Open your browser at `http://127.0.0.1:5000`

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `RESUME_VALIDATION_API_KEY` | Yes | Key for resume validation API |
| `RESUME_VALIDATION_API_URL` | Yes | URL for resume validation API |
| `GROQ_API_KEY` | No | Groq API key for AI suggestions |
| `SECRET_KEY` | Yes | Flask session secret key |

---

## How It Works

```
Upload Resume
     ↓
Validate via API
     ↓
Extract Text (PDF/DOCX)
     ↓
Clean Text (preserve c++, node.js, ci/cd)
     ↓
Match Skills (regex word-boundary + synonyms)
     ↓
Detect Sections
     ↓
Generate AI Suggestions (Groq API)
     ↓
Display Results
```

---

## License

MIT License — feel free to use, modify, and distribute.

---

<p align="center">Built by <a href="https://github.com/sanjana-chetry">Sanjana Chetry</a></p>
