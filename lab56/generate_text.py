import requests
import time
from concurrent.futures import ThreadPoolExecutor


API_KEY = "api_key"

TOTAL_SENTENCES = 9000
BATCH_SIZE = 250
CONCURRENCY = 16
MODEL = "x-ai/grok-4.1-fast"
TEMPERATURE = 0.9
OUTPUT_FILE = "lab56/sentences_az.txt"


def generate_batch():
    """Send one request to the API and return list of sentences."""
    prompt = f"""
Generate exactly {BATCH_SIZE} sentences in the Azerbaijani language that strictly comply with the following requirements:
REMEMBER EACH SENTENCE SHOULD CONTAIN TEN WORDS AT LEAST!!!

1. Each sentence must be meaningful and logically correct.
2. Each sentence must be written in Azerbaijani only.
3. Each sentence must start with a capital letter and end with a period.
4. The minimum length is ten words, and the maximum length is fifteen words.
5. Do not use digits or abbreviations. Everything must be fully written out in words.
6. Each sentence must be unique.
7. Each sentence must be on a separate line.
8. Do not use extra punctuation (no commas, enumeration, etc). Only words and the final period.
9. Do not include any description or instructions — output only sentences.

REMEMBER EACH SENTENCE SHOULD CONTAIN TEN WORDS AT LEAST!!!

Return only the sentences.
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You strictly follow instructions."},
            {"role": "user", "content": prompt}
        ],
        "temperature": TEMPERATURE
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            return content.split("\n")
        else:
            print(f"API Error: {response.text}")
            return []
    except Exception as e:
        print(f"Request failed: {e}")
        return []


def is_valid(sentence):
    sentence = sentence.strip()
    if not sentence.endswith("."):
        return False
    return len(sentence[:-1].split()) >= 7


def main():
    if not API_KEY:
        print("Please insert your API key!")
        return

    sentences = set()

    print("\nStarting parallel generation...")

    while len(sentences) < TOTAL_SENTENCES:
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
            results = executor.map(lambda _: generate_batch(), range(CONCURRENCY))

        for batch in results:
            valid = [s for s in batch if is_valid(s)]
            sentences.update(valid)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(sentences))

        print(f"Progress: {len(sentences)} / {TOTAL_SENTENCES}")
        time.sleep(1)

    print("\nGeneration complete!")
    print(f"Total sentences: {len(sentences)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
