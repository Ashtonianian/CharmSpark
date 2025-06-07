import os
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
import re

# Configuration
PROJECT_NAME = "CharmSpark"
SOURCE_DIR = Path(__file__).resolve().parent.parent / "Source" / PROJECT_NAME

app = FastAPI()

# Models for API
class Property(BaseModel):
    type: str
    name: str

class Function(BaseModel):
    name: str

class ClassRequest(BaseModel):
    classname: str
    parent: str
    properties: List[Property]
    functions: List[Function]

class EditRequest(BaseModel):
    classname: str
    properties: List[str] = []
    functions: List[str] = []
    includes: List[str] = []

def clean_includes(header_text):
    """Ensure includes are after #pragma once"""
    pragma_idx = header_text.find("#pragma once")
    lines = header_text.splitlines()
    if pragma_idx == -1:
        return header_text  # fallback

    pragma_line = None
    for i, line in enumerate(lines):
        if "#pragma once" in line:
            pragma_line = i
            break

    includes = [line for line in lines if line.startswith("#include")]
    other_lines = [line for i, line in enumerate(lines) if not line.startswith("#include") or i <= pragma_line]

    cleaned = other_lines[:pragma_line+1] + includes + other_lines[pragma_line+1:]
    return "\n".join(cleaned)

def fix_property_formatting(header_text):
    # Fix UPROPERTY declarations smashed together
    # Makes sure each UPROPERTY starts on its own line with proper spacing
    return re.sub(r';\s*(UPROPERTY\(.*?\))', r';\n    \1', header_text)


@app.post("/create_class")
def create_class(request: ClassRequest):
    success = generate_code(request.classname, request.parent, request.properties, request.functions)
    if not success:
        return {"error": "Class already exists"}
    return {"status": "Class created"}

@app.post("/edit_class")
def edit_class(data: EditRequest):
    header_path = SOURCE_DIR / f"{data.classname}.h"
    source_path = SOURCE_DIR / f"{data.classname}.cpp"

    if not header_path.exists() or not source_path.exists():
        return {"error": "Class does not exist."}


    header_text = header_path.read_text()
    source_text = source_path.read_text()

    for inc in data.includes:
        if inc not in header_text:
            header_text = f'#include "{inc}"\n' + header_text

    for prop in data.properties:
        if prop not in header_text:
            match = re.search(r'(UCLASS\(\)[\s\S]*?GENERATED_BODY\(\)\s*)', header_text)
            if match:
                insert_point = match.end()
                header_text = header_text[:insert_point] + f'\n    UPROPERTY(EditAnywhere, BlueprintReadWrite)\n    {prop};\n' + header_text[insert_point:]

    for func in data.functions:
        if f'void {func}();' not in header_text:
            header_text += f'\n    UFUNCTION(BlueprintCallable)\n    void {func}();'

    for func in data.functions:
        if f'void {data.classname}::{func}()' not in source_text:
            if func.lower() == "look":
                source_text += f'\nvoid {data.classname}::Look() {{\n    AddControllerYawInput(1.0f);\n}}\n'
            else:
                source_text += f'\nvoid {data.classname}::{func}() {{\n    // TODO: Implement {func}\n}}\n'

    # Clean header format
    header_text = clean_includes(header_text)
    header_text = fix_property_formatting(header_text)

    header_path.write_text(header_text)
    source_path.write_text(source_text)

    return {"message": f"{data.classname} updated successfully."}


def generate_code(class_name, parent_class, props, funcs):
    header_path = SOURCE_DIR / f"{class_name}.h"
    source_path = SOURCE_DIR / f"{class_name}.cpp"

    if header_path.exists() or source_path.exists():
        print("⚠️  Class already exists. Delete it first or choose another name.")
        return False

    class_declaration = f"""#pragma once

#include \"{parent_class}.h\"
#include \"CoreMinimal.h\"
#include \"{class_name}.generated.h\"

UCLASS()
class {PROJECT_NAME.upper()}_API {class_name} : public {parent_class}
{{
    GENERATED_BODY()

public:
    {class_name}();

protected:
    virtual void BeginPlay() override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

public:
    virtual void Tick(float DeltaTime) override;

{''.join([f'    UPROPERTY(EditAnywhere, BlueprintReadWrite)\n    {p.type} {p.name};\n\n' for p in props])}
{''.join([f'    UFUNCTION(BlueprintCallable)\n    void {f.name}();\n\n' for f in funcs])}
}};
"""

    class_definition = f"""#include \"{class_name}.h\"

{class_name}::{class_name}() {{
    PrimaryActorTick.bCanEverTick = true;
}}

void {class_name}::BeginPlay() {{
    Super::BeginPlay();
}}

void {class_name}::Tick(float DeltaTime) {{
    Super::Tick(DeltaTime);
}}

{''.join([f'void {class_name}::{f.name}() {{}}\n\n' for f in funcs])}
"""

    os.makedirs(SOURCE_DIR, exist_ok=True)
    header_path.write_text(class_declaration)
    source_path.write_text(class_definition)
    print(f"✅ Created: {class_name}.h and {class_name}.cpp")
    return True

if __name__ == "__main__":
    uvicorn.run("class_api:app", host="127.0.0.1", port=8000, reload=True)
