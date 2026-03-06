import json
import os
import re

# Load skills once (when file is imported)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_PATH = os.path.join(BASE_DIR, "role_skills.json")

with open(SKILL_PATH, "r", encoding="utf-8") as f:
    ROLE_SKILLS = json.load(f)


def detect_skills(resume_text, selected_role):
    """
    Detect matched and missing skills for a given role.
    Supports structured skills with synonyms.
    Handles special characters like c++, node.js, ci/cd properly.
    """

    # Validate role
    if selected_role not in ROLE_SKILLS:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "error": "Invalid role selected"
        }

    role_skills = ROLE_SKILLS[selected_role]

    # Normalize resume text
    resume_text = resume_text.lower()

    # Better tokenization (handles c++, node.js, ci/cd, scikit-learn, etc.)
    resume_tokens = set(resume_text.split())
    
    matched = []
    missing = []

    for skill_obj in role_skills:
        skill_name = skill_obj["name"].lower()
        synonyms = [s.lower() for s in skill_obj.get("synonyms", [])]

        found = False

        # ---------- Check main skill ----------
        if " " in skill_name:
            if skill_name in resume_text:
                found = True
        else:
            if skill_name in resume_tokens:
                found = True

        # ---------- Check synonyms if not found ----------
        if not found:
            for syn in synonyms:
                if " " in syn:
                    if syn in resume_text:
                        found = True
                        break
                else:
                    if syn in resume_tokens:
                        found = True
                        break

        # ---------- Store canonical skill name ----------
        if found:
            matched.append(skill_name)
        else:
            missing.append(skill_name)

    return {
        "matched_skills": matched,
        "missing_skills": missing
    }