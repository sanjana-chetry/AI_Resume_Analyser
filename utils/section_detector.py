"""
section_detector.py
-------------------
Scans raw resume text for common section headings and returns
a list of sections found and not found.
"""

# Each section has a name and a list of keywords to look for.
# If ANY keyword is found in the resume text, the section is marked as present.
SECTIONS = [
    {
        "name": "Education",
        "keywords": ["education", "academic", "university", "college", "degree", "bachelor", "master", "b.tech", "b.sc", "m.tech", "m.sc", "school"]
    },
    {
        "name": "Experience",
        "keywords": ["experience", "work experience", "employment", "internship", "intern", "worked at", "job"]
    },
    {
        "name": "Skills",
        "keywords": ["skills", "technical skills", "core skills", "competencies", "technologies", "tools"]
    },
    {
        "name": "Projects",
        "keywords": ["projects", "personal projects", "academic projects", "project work", "portfolio"]
    },
    {
        "name": "Certifications",
        "keywords": ["certifications", "certificates", "certified", "certification", "courses", "training"]
    },
    {
        "name": "Achievements",
        "keywords": ["achievements", "awards", "honours", "honors", "accomplishments", "recognition"]
    },
    {
        "name": "Summary",
        "keywords": ["summary", "objective", "profile", "about me", "career objective", "professional summary"]
    },
]


def detect_sections(raw_text: str) -> list:
    """
    Detect which resume sections are present in the raw text.

    Parameters
    ----------
    raw_text : str — Raw (uncleaned) resume text

    Returns
    -------
    list of dicts, each with:
        - name    : str   — Section name e.g. "Education"
        - found   : bool  — Whether it was detected in the resume
    """
    text_lower = raw_text.lower()

    results = []
    for section in SECTIONS:
        # Check if any keyword for this section appears in the text
        found = any(keyword in text_lower for keyword in section["keywords"])
        results.append({
            "name": section["name"],
            "found": found
        })

    return results
