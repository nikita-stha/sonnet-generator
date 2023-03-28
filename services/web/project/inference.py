import os
import json
import requests

API_URL = "https://api-inference.huggingface.co/models/niki-stha/gpt2-sonnet-generators"


def query(data):
    headers = {"Authorization": "Bearer " + os.environ["HUGGINGFACE_INFERENCE_API_TOKEN"]}
    try:
        data = json.dumps(data)
        response = requests.post(API_URL, headers=headers, data=data,)
        response = response.json()
        return response
    except:
        return response
