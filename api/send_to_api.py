import requests

def send_to_api(image_path):
    url = "https://api.brickognize.com/predict/"
    files = {"query_image": open(image_path, "rb")}
    headers = {"accept": "application/json"}
    response = requests.post(url, files=files, headers=headers)
    return response.json()