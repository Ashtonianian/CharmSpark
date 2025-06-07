import requests

data = {
    "classname": "APlayerCharacter",
    "properties": ["float Speed"],
    "functions": ["Look"],
    "includes": ["GameFramework/Actor.h"]
}

response = requests.post("http://localhost:8000/edit_class", json=data)
print(response.json())
