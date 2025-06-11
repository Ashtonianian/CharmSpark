// === APlayerCharacter.cpp ===
#include "APlayerCharacter.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/InputComponent.h"
#include "Blueprint/UserWidget.h"
#include "AEnemyCharacter.h"



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
    SpringArm->DestroyComponent(); // optional


    FirstPersonCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FirstPersonCamera"));
    FirstPersonCamera->SetupAttachment(RootComponent); // Or CapsuleComponent if needed
    FirstPersonCamera->bUsePawnControlRotation = true;
    FirstPersonCamera->SetRelativeLocation(FVector(0.f, 0.f, 64.f)); // Rough eye height





    // Load skeletal mesh from content
    static ConstructorHelpers::FObjectFinder<USkeletalMesh> MeshAsset(TEXT("SkeletalMesh'/Game/Characters/Player/HeroModel/BobaFett.BobaFett'"));


    if (MeshAsset.Succeeded())
    {
        GetMesh()->SetSkeletalMesh(MeshAsset.Object);

        // Position the mesh (important!)
        GetMesh()->SetRelativeLocation(FVector(0.0f, 0.0f, -90.0f)); // adjust as needed
        GetMesh()->SetRelativeRotation(FRotator(0.0f, -90.0f, 0.0f)); // faces forward
    }

    static ConstructorHelpers::FClassFinder<UUserWidget> CrosshairClass(TEXT("/Game/UI/WBP_Crosshair")); // Adjust path as needed
    if (CrosshairClass.Succeeded())
    {
        CrosshairWidgetClass = CrosshairClass.Class;
    }


}

void APlayerCharacter::BeginPlay()
{
    Super::BeginPlay();

    if (UWorld* World = GetWorld())
    {
        FVector SpawnLocation = GetActorLocation() + FVector(500.0f, 0.0f, 0.0f); // Spawn 500 units in front
        FRotator SpawnRotation = GetActorRotation();

        FActorSpawnParameters SpawnParams;
        SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AdjustIfPossibleButAlwaysSpawn;

        World->SpawnActor<AEnemyCharacter>(AEnemyCharacter::StaticClass(), SpawnLocation, SpawnRotation, SpawnParams);
    }


    if (APlayerController* PC = Cast<APlayerController>(GetController()))
    {
        if (CrosshairWidgetClass) // UPROPERTY pointing to your Widget Blueprint
        {
            UUserWidget* Crosshair = CreateWidget<UUserWidget>(PC, CrosshairWidgetClass);
            if (Crosshair)
            {
                Crosshair->AddToViewport();
            }
        }
    }

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

    PlayerInputComponent->BindAction("Melee", IE_Pressed, this, &APlayerCharacter::DoMelee);

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

void APlayerCharacter::DoMelee()
{
    FVector Start = FirstPersonCamera->GetComponentLocation();
    FVector Forward = FirstPersonCamera->GetForwardVector();
    FVector End = Start + (Forward * 150.0f);



    FHitResult Hit;
    FCollisionQueryParams Params;
    Params.AddIgnoredActor(this); // Don't hit self

    bool bHit = GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_Pawn, Params);

    if (bHit)
    {
        UE_LOG(LogTemp, Warning, TEXT("Melee hit: %s at %s"), *Hit.GetActor()->GetName(), *Hit.ImpactPoint.ToString());

        // You can use Hit.ImpactPoint here as your adjustable vector


    }
    else
    {
        UE_LOG(LogTemp, Warning, TEXT("Melee missed"));


    }



    // Optional: Draw debug line
    DrawDebugLine(GetWorld(), Start, End, FColor::Red, false, 1.0f, 0, 2.0f);
}
