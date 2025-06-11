import requests

data = {
    "classname": "AEnemyCharacter",
    "properties": [
        "float Health = 100.0f"
    ],
    "functions": [
        {
            "signature": "float TakeDamage(float DamageAmount, const FDamageEvent& DamageEvent, AController* EventInstigator, AActor* DamageCauser) override",
            "body": """Health -= DamageAmount;
UE_LOG(LogTemp, Warning, TEXT("Enemy took damage! Health: %f"), Health);
if (Health <= 0.0f) {
    UE_LOG(LogTemp, Warning, TEXT("Enemy died"));
    Destroy();
}
return DamageAmount;"""
        }
    ],
    "includes": [
        "GameFramework/Character.h",
        "Kismet/GameplayStatics.h"
    ]
}

response = requests.post("http://localhost:8000/edit_class", json=data)
print(response.json())
