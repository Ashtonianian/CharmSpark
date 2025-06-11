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

# === Models ===
class Function(BaseModel):
    signature: str  # Full declaration for header
    body: str       # Only body content

class EditRequest(BaseModel):
    classname: str
    properties: List[str] = []
    functions: List[Function] = []
    includes: List[str] = []

class CreateClassRequest(BaseModel):
    classname: str
    baseclass: str = "AActor"
    includes: List[str] = []
    use_tick: bool = True

# === Helpers ===
def fix_property_formatting(header_text):
    return re.sub(r';\s*UPROPERTY', ';\n    UPROPERTY', header_text)

# === ROUTE: Create Class ===
@app.post("/create_class")
def create_class(data: CreateClassRequest):
    header_path = SOURCE_DIR / f"{data.classname}.h"
    source_path = SOURCE_DIR / f"{data.classname}.cpp"

    if header_path.exists() or source_path.exists():
        return {"error": "Header or source file already exists."}

    includes = '\n'.join([f'#include "{inc}"' for inc in data.includes])
    tick_line = "virtual void Tick(float DeltaTime) override;" if data.use_tick else ""

    header_content = f"""#pragma once

{includes}

#include "CoreMinimal.h"
#include "{data.baseclass}.h"
#include "{data.classname}.generated.h"

UCLASS()
class {PROJECT_NAME.upper()}_API {data.classname} : public {data.baseclass}
{{
    GENERATED_BODY()

public:
    {data.classname}();
    {tick_line}
}};
"""

    source_content = f"""#include "{data.classname}.h"

{data.classname}::{data.classname}() {{
    PrimaryActorTick.bCanEverTick = {"true" if data.use_tick else "false"};
}}

{"void " + data.classname + "::Tick(float DeltaTime) {\n    Super::Tick(DeltaTime);\n}\n" if data.use_tick else ""}
"""

    header_path.write_text(header_content)
    source_path.write_text(source_content)

    return {"message": f"{data.classname} created successfully."}

# === ROUTE: Edit Class ===
@app.post("/edit_class")
def edit_class(data: EditRequest):
    header_path = SOURCE_DIR / f"{data.classname}.h"
    source_path = SOURCE_DIR / f"{data.classname}.cpp"

    if not header_path.exists() or not source_path.exists():
        return {"error": f"Class {data.classname} does not exist at expected location."}

    header_text = header_path.read_text()
    source_text = source_text = source_path.read_text()

    # === Add includes ===
    for inc in data.includes:
        include_line = f'#include "{inc}"'
        if include_line not in header_text:
            header_text = include_line + "\n" + header_text

    # === Add properties ===
    for prop in data.properties:
        if prop not in header_text:
            match = re.search(r'(public:\s*)', header_text)
            if match:
                insert_point = match.end()
                header_text = (
                    header_text[:insert_point] +
                    f'\n    UPROPERTY(EditAnywhere, BlueprintReadWrite)\n    {prop};' +
                    header_text[insert_point:]
                )

    # === Add functions ===
    for func in data.functions:
        if func.signature not in header_text:
            header_text = re.sub(
                r'(};)',
                f'    UFUNCTION(BlueprintCallable)\n    {func.signature};\n' + r'\1',
                header_text,
                count=1
            )

        func_name_match = re.match(r'.+? (\w+)\(', func.signature)
        func_name = func_name_match.group(1) if func_name_match else None

        if func_name and func_name not in source_text:
            source_text += f"\n{func.signature}\n{{\n{func.body}\n}}\n"

    # Final formatting cleanup
    header_text = fix_property_formatting(header_text)

    header_path.write_text(header_text)
    source_path.write_text(source_text)

    return {"message": f"{data.classname} updated successfully."}

if __name__ == "__main__":
    uvicorn.run("class_api:app", host="127.0.0.1", port=8000, reload=True)
