import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:1.7b"


def generate_response(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "format": "json",
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()["response"]