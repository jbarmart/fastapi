import random
import requests
import json


def generate_random_metrics(base_url: str):
    endpoints = [
        {"method": "GET", "url": f"{base_url}/get_user/{random.randint(1, 100)}"},
        {"method": "POST", "url": f"{base_url}/create_user",
         "data": {"user_id": random.randint(1, 100), "username": "user_" + str(random.randint(1, 100))}},
        {"method": "PUT", "url": f"{base_url}/update_user?user_id={random.randint(1, 100)}",
         "data": {"user_id": random.randint(1, 100), "username": "updated_user_" + str(random.randint(1, 100))}},
        {"method": "GET", "url": f"{base_url}/health"}
    ]

    for _ in range(25):  # Number of requests to send
        endpoint = random.choice(endpoints)
        method = endpoint["method"]
        url = endpoint["url"]
        data = endpoint.get("data", None)

        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
            elif method == "PUT":
                response = requests.put(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))

            # Print response for debugging
            print(f"{method} {url} -> Status Code: {response.status_code}")

        except requests.RequestException as e:
            print(f"Error {method} {url}: {e}")


# Example usage:
if __name__ == '__main__':
    generate_random_metrics("http://localhost:8080")