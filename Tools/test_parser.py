import requests

response = requests.post("http://127.0.0.1:8000/edit_class", json={
    "classname": "APlayerCharacter",
    "properties": [
        "float CrouchSpeed",
        "bool bIsCrouching"
    ],
    "functions": [
        "StartCrouching",
        "StopCrouching"
    ],
    "includes": [
        "GameFramework/CharacterMovementComponent.h"
    ]
})

print(response.json())
