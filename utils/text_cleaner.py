"""
text_cleaner.py
---------------
Cleans raw resume text before skill detection.
Preserves technical characters like +, #, ., -, /
so skills like c++, node.js, ci/cd are not destroyed.
"""

import re


def clean_text(text: str) -> str:
    """
    Clean and normalise raw resume text for skill matching.

    Steps:
    1. Lowercase
    2. Remove URLs
    3. Remove email addresses
    4. Remove all characters except letters, digits, and tech symbols
    5. Collapse extra whitespace
    """

    # 1. Lowercase everything
    text = text.lower()

    # 2. Remove URLs (http://... and www....)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # 3. Remove email addresses (anything with @ in the middle)
    text = re.sub(r"\S+@\S+", " ", text)

    # 4. Remove characters that are not useful for skill matching.
    #    Keep: word chars (\w), whitespace (\s), and + # . - /
    #    This preserves: c++, c#, node.js, ci/cd, scikit-learn, etc.
    text = re.sub(r"[^\w\s\+\#\.\-\/]", " ", text)

    # 5. Collapse multiple spaces/newlines into a single space
    text = re.sub(r"\s+", " ", text)

    return text.strip()
