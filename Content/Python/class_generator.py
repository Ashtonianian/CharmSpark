import unreal

def create_cpp_class(class_name, parent_class="Actor"):
    unreal.EditorAssetLibrary.save_all_dirty_packages()
    tools = unreal.SystemLibrary.get_engine_version()
    
    unreal.PythonScriptLibrary.create_new_cpp_class(
        base_class=parent_class,
        class_name=class_name,
        module_name="CharmSpark"
    )
    print(f"[✔] Created class: {class_name}")

# Example usage:
create_cpp_class("MyNewActor", "Actor")
