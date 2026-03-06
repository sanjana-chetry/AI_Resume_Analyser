import re

def clean_text(text):
    # convert to lowercase
    text = text.lower()

    # remove special characters (keep letters & numbers)
    text = re.sub(r"[^a-z0-9\s\+\#\.\-\/]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()
