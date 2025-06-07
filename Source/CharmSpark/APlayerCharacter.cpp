// === APlayerCharacter.cpp ===
#include "APlayerCharacter.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/InputComponent.h"

APlayerCharacter::APlayerCharacter()
{
    PrimaryActorTick.bCanEverTick = true;

    GetCharacterMovement()->MaxWalkSpeed = MoveSpeed;
    GetCharacterMovement()->JumpZVelocity = 420.f;
    GetCharacterMovement()->GravityScale = 0.9f; // Adjust gravity scale here

    GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;
    GetCharacterMovement()->GetNavAgentPropertiesRef().bCanCrouch = true;

    SpringArm = CreateDefaultSubobject<USpringArmComponent>(TEXT("SpringArm"));
    SpringArm->SetupAttachment(RootComponent);
    SpringArm->TargetArmLength = 300.f; // Distance from player
    SpringArm->bUsePawnControlRotation = true;
    SpringArm->SetRelativeLocation(FVector(0.f, 0.f, 120.f)); // Raise the camera position

    Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
    Camera->SetupAttachment(SpringArm);
    Camera->bUsePawnControlRotation = false;



}

void APlayerCharacter::BeginPlay()
{
    Super::BeginPlay();
}

void APlayerCharacter::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
}

void APlayerCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    PlayerInputComponent->BindAxis("MoveForward", this, &APlayerCharacter::MoveForward);
    PlayerInputComponent->BindAxis("MoveRight", this, &APlayerCharacter::MoveRight);

    PlayerInputComponent->BindAction("Jump", IE_Pressed, this, &ACharacter::Jump);
    PlayerInputComponent->BindAction("Jump", IE_Released, this, &ACharacter::StopJumping);

    PlayerInputComponent->BindAxis("Turn", this, &APlayerCharacter::TurnAtRate);
    PlayerInputComponent->BindAxis("LookUp", this, &APlayerCharacter::LookUpAtRate);

    PlayerInputComponent->BindAction("Sprint", IE_Pressed, this, &APlayerCharacter::StartSprinting);
    PlayerInputComponent->BindAction("Sprint", IE_Released, this, &APlayerCharacter::StopSprinting);

    PlayerInputComponent->BindAction("Crouch", IE_Pressed, this, &APlayerCharacter::StartCrouching);
    PlayerInputComponent->BindAction("Crouch", IE_Released, this, &APlayerCharacter::StopCrouching);

}

void APlayerCharacter::MoveForward(float Value)
{
    AddMovementInput(GetActorForwardVector(), Value);
}

void APlayerCharacter::MoveRight(float Value)
{
    AddMovementInput(GetActorRightVector(), Value);
}

void APlayerCharacter::Look()
{
    // Not used directly unless you bind this manually
}

void APlayerCharacter::TurnAtRate(float Value)
{
    AddControllerYawInput(Value * 0.5f); // Lower this number for lower sensitivity
}

void APlayerCharacter::LookUpAtRate(float Value)
{
    AddControllerPitchInput(Value * 0.5f);
}

void APlayerCharacter::StartSprinting() {
    // TODO: Implement StartSprinting

    GetCharacterMovement()->MaxWalkSpeed = SprintSpeed;
}

void APlayerCharacter::StopSprinting() {
    // TODO: Implement StopSprinting

    GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;
}

void APlayerCharacter::StartCrouching() {
    if (!bIsCrouching) {
        Crouch();
        bIsCrouching = true;
        GetCharacterMovement()->MaxWalkSpeed = CrouchSpeed; 300.f;
    }
}

void APlayerCharacter::StopCrouching() {
    if (bIsCrouching) {
        UnCrouch();
        bIsCrouching = false;
        GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;
    }
}
