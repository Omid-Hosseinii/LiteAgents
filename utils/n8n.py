import requests


N8N_WEBHOOK_URL = ("http://localhost:5678/webhook/3c6dd504-7d0f-4ec1-8d51-3b421d21fc32")


def trigger_workflow():
    response = requests.post(
        N8N_WEBHOOK_URL,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


trigger_workflow()
