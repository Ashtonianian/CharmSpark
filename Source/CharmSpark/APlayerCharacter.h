// === APlayerCharacter.h ===
#pragma once

#include "Camera/CameraComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
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

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
    class USpringArmComponent* SpringArm;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
    class UCameraComponent* Camera;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bIsCrouching;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float CrouchSpeed;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Movement")
    float MoveSpeed = 600.f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Movement")
    float WalkSpeed = 600.f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Movement")
    float SprintSpeed = 1200.f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bIsSprinting;

    UFUNCTION(BlueprintCallable)
    void Look();

    void MoveForward(float Value);
    void MoveRight(float Value);

    UFUNCTION(BlueprintCallable)
    void TurnAtRate(float Value);

    UFUNCTION(BlueprintCallable)
    void LookUpAtRate(float Value);

    UFUNCTION(BlueprintCallable)
    void StartSprinting();

    UFUNCTION(BlueprintCallable)
    void StopSprinting();

    UFUNCTION(BlueprintCallable)
    void StartCrouching();

    UFUNCTION(BlueprintCallable)
    void StopCrouching();

    UFUNCTION()
    void DoMelee();

};
