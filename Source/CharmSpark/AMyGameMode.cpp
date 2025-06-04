// === AMyGameMode.cpp ===
#include "AMyGameMode.h"
#include "UObject/ConstructorHelpers.h"
#include "APlayerCharacter.h"

AMyGameMode::AMyGameMode()
{
    DefaultPawnClass = APlayerCharacter::StaticClass();
    PrimaryActorTick.bCanEverTick = true;
}

void AMyGameMode::BeginPlay()
{
    Super::BeginPlay();
}

void AMyGameMode::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
}
