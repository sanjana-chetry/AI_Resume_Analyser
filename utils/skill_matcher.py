"""
skill_matcher.py
----------------
Detects matched and missing skills for a given role.
Uses regex word-boundary matching to avoid false positives
e.g. 'java' matching inside 'javascript'.
"""

import json
import os
import re

# Load role skills once when this file is first imported
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_PATH = os.path.join(BASE_DIR, "role_skills.json")

with open(SKILL_PATH, "r", encoding="utf-8") as f:
    ROLE_SKILLS = json.load(f)


def _skill_found(skill: str, resume_text: str) -> bool:
    """
    Check if a skill exists in the resume text.

    For multi-word skills (e.g. "machine learning"):
        Uses simple substring search — phrases won't accidentally
        match inside another word.

    For single-word skills (e.g. "java", "c++", "node.js"):
        Uses regex with word boundaries so "java" does NOT match
        inside "javascript", and special chars like + are handled safely.
    """
    skill = skill.lower()

    if " " in skill:
        # Multi-word: plain substring check is safe and sufficient
        return skill in resume_text
    else:
        # Single-word: word-boundary regex
        # re.escape() makes special chars like +, ., / safe for regex
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        return bool(re.search(pattern, resume_text))


def detect_skills(resume_text: str, selected_role: str) -> dict:
    """
    Compare resume text against the required skills for a role.

    Parameters
    ----------
    resume_text   : str — Cleaned resume text
    selected_role : str — Role key matching a key in role_skills.json

    Returns
    -------
    dict with keys:
        matched_skills : list of skill names found in the resume
        missing_skills : list of skill names NOT found in the resume
        match_score    : int (0–100), percentage of role skills matched
    """

    if selected_role not in ROLE_SKILLS:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "match_score": 0,
            "error": f"Role '{selected_role}' not found."
        }

    role_skills = ROLE_SKILLS[selected_role]

    # Normalize resume text to lowercase once
    resume_text = resume_text.lower()

    matched = []
    missing = []

    for skill_obj in role_skills:
        skill_name = skill_obj["name"]
        synonyms = skill_obj.get("synonyms", [])

        found = False

        # Check main skill name
        if _skill_found(skill_name, resume_text):
            found = True

        # Check synonyms if main skill was not found
        if not found:
            for syn in synonyms:
                if _skill_found(syn, resume_text):
                    found = True
                    break

        # Store the canonical skill name (from JSON), not the synonym
        if found:
            matched.append(skill_obj["name"])
        else:
            missing.append(skill_obj["name"])

    # Calculate percentage score
    total = len(role_skills)
    score = round((len(matched) / total) * 100) if total > 0 else 0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_score": score
    }
