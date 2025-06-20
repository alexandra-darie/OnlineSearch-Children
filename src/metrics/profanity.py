from better_profanity import profanity
import requests
import os
import base64

# Decode LDNOOBW list
def load_bad_words_from_base64_file(filepath):
    with open(filepath, "rb") as file:
        encoded = file.read()
        decoded = base64.b64decode(encoded).decode("utf-8")
        return set(word.strip().lower() for word in decoded.splitlines() if word.strip())

base_dir = os.path.dirname(os.path.abspath(__file__))
base64_path = os.path.join(base_dir, "../../LDNOOBW_BASE64.txt")
BAD_WORDS = load_bad_words_from_base64_file(base64_path)

profanity.load_censor_words()

def contains_model_profanity(text):
    return profanity.contains_profanity(text)

def contains_ldnoobw_profanity(text):
    words = set(text.lower().split())
    return not BAD_WORDS.isdisjoint(words)

# Calculate profanity using both techniques
def contains_profanity(text):
    return contains_model_profanity(text) or contains_ldnoobw_profanity(text)