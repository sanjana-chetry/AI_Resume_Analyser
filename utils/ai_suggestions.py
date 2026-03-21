"""
ai_suggestions.py
-----------------
Uses the Groq API (free) to generate one-line resume improvement
suggestions for each missing skill.

Requires GROQ_API_KEY in your .env file.
Get a free key at: console.groq.com
"""

import os
import json
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def get_suggestions(missing_skills: list) -> list:
    """
    For each missing skill, generate a short actionable resume tip.

    Returns empty list if no skills are missing, key is not set,
    or the API call fails for any reason.
    """

    if not missing_skills:
        return []

    if not GROQ_API_KEY:
        return []

    skills_list = "\n".join(f"- {skill}" for skill in missing_skills)

    prompt = f"""You are a resume improvement assistant. A candidate is missing the following skills for their target job role:

{skills_list}

For each missing skill, write exactly ONE short practical sentence (max 15 words) telling the candidate how to add this skill to their resume. Focus on concrete actions like adding a project, listing a tool, or mentioning coursework.

Respond ONLY with a valid JSON array. No explanation, no markdown, no extra text.
Format:
[
  {{"skill": "skill name", "suggestion": "your one-line tip here"}},
  ...
]"""

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.4,
                "max_tokens": 1000
            },
            timeout=20
        )

        data = response.json()

        # Extract text from Groq's response structure
        raw_text = data["choices"][0]["message"]["content"].strip()

        # Remove markdown code fences if model wraps in ```json ... ```
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]

        suggestions = json.loads(raw_text.strip())
        return suggestions

    except Exception:
        # If anything fails, return empty list gracefully
        return []
