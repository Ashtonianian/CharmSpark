
import os
import sys
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Generate or delete Unreal C++ class files")
parser.add_argument("classname", help="Name of the class to generate or delete")
parser.add_argument("parent", nargs="?", default="AActor", help="Parent class (default: AActor)")
parser.add_argument("--prop", action="append", default=[], help="Properties (e.g. float MoveSpeed)")
parser.add_argument("--func", action="append", default=[], help="Functions (e.g. Jump)")
parser.add_argument("--type", help="Special class type (e.g. character)")
parser.add_argument("--delete", action="store_true", help="Delete the class files instead")
args = parser.parse_args()

class_name = args.classname
parent_class = args.parent
properties = args.prop
functions = args.func
project_root = Path(__file__).resolve().parents[1]
source_path = project_root / "Source" / project_root.name
header_path = source_path / f"{class_name}.h"
cpp_path = source_path / f"{class_name}.cpp"

if args.delete:
    try:
        deleted = []
        if header_path.exists():
            header_path.unlink()
            deleted.append(header_path.name)
        if cpp_path.exists():
            cpp_path.unlink()
            deleted.append(cpp_path.name)
        print(f"Deleted files: {', '.join(deleted) if deleted else 'None'}")
        sys.exit()
    except Exception as e:
        print(f"Error deleting files: {e}")
        sys.exit()

# Handle special case for character class
if args.type == "character":
    header_content = f"""#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "{class_name}.generated.h"

UCLASS()
class {project_root.name.upper()}_API {class_name} : public ACharacter
{{
    GENERATED_BODY()

public:
    {class_name}();

protected:
    virtual void BeginPlay() override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

public:
    virtual void Tick(float DeltaTime) override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Movement")
    float MoveSpeed = 600.0f;

    void MoveForward(float Value);
    void MoveRight(float Value);
}};
"""

    cpp_content = f"""#include "{class_name}.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/InputComponent.h"

{class_name}::{class_name}()
{{
    PrimaryActorTick.bCanEverTick = true;
    GetCharacterMovement()->MaxWalkSpeed = MoveSpeed;
    GetCharacterMovement()->JumpZVelocity = 600.0f;
}}

void {class_name}::BeginPlay()
{{
    Super::BeginPlay();
}}

void {class_name}::Tick(float DeltaTime)
{{
    Super::Tick(DeltaTime);
}}

void {class_name}::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{{
    Super::SetupPlayerInputComponent(PlayerInputComponent);
    PlayerInputComponent->BindAxis("MoveForward", this, &{class_name}::MoveForward);
    PlayerInputComponent->BindAxis("MoveRight", this, &{class_name}::MoveRight);
    PlayerInputComponent->BindAction("Jump", IE_Pressed, this, &ACharacter::Jump);
    PlayerInputComponent->BindAction("Jump", IE_Released, this, &ACharacter::StopJumping);
}}

void {class_name}::MoveForward(float Value)
{{
    AddMovementInput(GetActorForwardVector(), Value);
}}

void {class_name}::MoveRight(float Value)
{{
    AddMovementInput(GetActorRightVector(), Value);
}}
"""
else:
    # General class generation
    uproperty_block = ""
    for prop in properties:
        uproperty_block += f'    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Generated")\n    {prop};\n\n'

    ufunction_decl = ""
    for func in functions:
        ufunction_decl += f'    UFUNCTION(BlueprintCallable, Category="Generated")\n    void {func}();\n\n'

    header_content = f"""#pragma once

#include "CoreMinimal.h"
#include "GameFramework/{parent_class}.h"
#include "{class_name}.generated.h"

UCLASS()
class {project_root.name.upper()}_API {class_name} : public {parent_class}
{{
    GENERATED_BODY()

public:
    {class_name}();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

{uproperty_block}{ufunction_decl}}};
"""

    ufunction_body = ""
    for func in functions:
        ufunction_body += f"""void {class_name}::{func}()\n{{\n    UE_LOG(LogTemp, Warning, TEXT("{class_name}::{func} called!"));\n}}\n\n"""

    cpp_content = f"""#include "{class_name}.h"

{class_name}::{class_name}()
{{
    PrimaryActorTick.bCanEverTick = true;
}}

void {class_name}::BeginPlay()
{{
    Super::BeginPlay();
}}

void {class_name}::Tick(float DeltaTime)
{{
    Super::Tick(DeltaTime);
}}

{ufunction_body}
"""

try:
    header_path.write_text(header_content, encoding="utf-8")
    cpp_path.write_text(cpp_content, encoding="utf-8")
    print(f"Created {class_name}.h and {class_name}.cpp")
except Exception as e:
    print(f"Error writing files: {e}")
