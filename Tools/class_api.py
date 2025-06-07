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

def fix_property_formatting(header_text):
    # Fix stacked UPROPERTY declarations
    return re.sub(r';\s*UPROPERTY', ';\n    UPROPERTY', header_text)

@app.post("/edit_class")
def edit_class(data: EditRequest):
    header_path = SOURCE_DIR / f"{data.classname}.h"
    source_path = SOURCE_DIR / f"{data.classname}.cpp"

    if not header_path.exists() or not source_path.exists():
        return {"error": "Class does not exist."}

    header_text = header_path.read_text()
    source_text = source_path.read_text()

    # Add includes
    for inc in data.includes:
        if inc not in header_text:
            header_text = f'#include "{inc}"\n' + header_text

    # Insert properties above the constructor
    for prop in data.properties:
        if prop not in header_text:
            match = re.search(r'(public:\s*)', header_text)
            if match:
                insert_point = match.end()
                header_text = (
                    header_text[:insert_point]
                    + f'\n    UPROPERTY(EditAnywhere, BlueprintReadWrite)\n    {prop};'
                    + header_text[insert_point:]
                )

    # Insert functions before the class closing brace
    for func in data.functions:
        if f'void {func}();' not in header_text:
            func_declaration = f'    UFUNCTION(BlueprintCallable)\n    void {func}();\n'
            header_text = re.sub(r'(};)', func_declaration + r'\1', header_text, count=1)

        if f'void {data.classname}::{func}()' not in source_text:
            if func == "Look":
                source_text += f'''
void {data.classname}::Look() {{
    AddControllerYawInput(1.0f);  // Example input logic
}}
'''
            else:
                source_text += f'''
void {data.classname}::{func}() {{
    // TODO: Implement {func}
}}
'''

    # Format any stacked UPROPERTYs just in case
    header_text = fix_property_formatting(header_text)

    header_path.write_text(header_text)
    source_path.write_text(source_text)

    return {"message": f"{data.classname} updated successfully."}

if __name__ == "__main__":
    uvicorn.run("class_api:app", host="127.0.0.1", port=8000, reload=True)
