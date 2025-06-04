// === AMyGameMode.h ===
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "AMyGameMode.generated.h"

UCLASS()
class CHARMSPARK_API AMyGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    AMyGameMode();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;
};