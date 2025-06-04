// === APlayerCharacter.h ===
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "APlayerCharacter.generated.h"

UCLASS()
class CHARMSPARK_API APlayerCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    APlayerCharacter();

protected:
    virtual void BeginPlay() override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

public:
    virtual void Tick(float DeltaTime) override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Movement")
    float MoveSpeed = 600.f;

    void MoveForward(float Value);
    void MoveRight(float Value);
};
