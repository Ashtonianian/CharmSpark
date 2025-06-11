import requests

data = {
    "classname": "AEnemyCharacter",
    "baseclass": "ACharacter",
    "includes": [
        "GameFramework/Character.h"
    ],
    "use_tick": True
}

response = requests.post("http://localhost:8000/create_class", json=data)
print(response.json())
