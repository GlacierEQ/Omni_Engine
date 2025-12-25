import requests
import json

api_key = "m0-bjuFyuiIvBcaj7c1KXSlUkogNPifL5GT2vU5zrjj"
url = "https://api.mem0.ai/v1/memories/"

headers = {
    "Authorization": f"Token {api_key}",
    "Content-Type": "application/json"
}

data = {
    "messages": [{"role": "user", "content": "Raw API Test: Aspen Grove case data."}],
    "user_id": "casey_test_001"
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
