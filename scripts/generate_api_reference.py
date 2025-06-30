import os
import sys
import inspect
import importlib
from pathlib import Path

def generate_api_docs(package_root, scan_dirs, output_file):
    """Inspects the source code and generates a Markdown API reference, including dynamically loaded methods."""
    sys.path.insert(0, os.path.abspath(package_root))

    docs = "# DW8 Code Atlas (API Reference)\n\n"
    docs += "This document is the single source of truth for the DW8 project's API. It is auto-generated from the source code's docstrings.\n\n---\n"

    # Define paths and filters for dynamically loaded methods
    DYNAMIC_METHOD_DIRS = {
        'WorkflowState': ('src/dw6/st', lambda f: not f.startswith('manager_') and not f.startswith('governor_') and not f.startswith('__')),
        'WorkflowManager': ('src/dw6/st', lambda f: f.startswith('manager_')),
        'Governor': ('src/dw6/st', lambda f: f.startswith('governor_')),
        'WorkflowKernel': ('src/dw6/workflow/kr', lambda f: not f.startswith('__')),
        'DeployerStage': ('src/dw6/workflow/dp', lambda f: not f.startswith('__')),
    }

    # Pre-calculate the set of all dynamic method files to avoid documenting them as standalone modules
    dynamic_files = set()
    for method_dir, file_filter in DYNAMIC_METHOD_DIRS.values():
        if os.path.isdir(method_dir):
            for file in os.listdir(method_dir):
                if file.endswith('.py') and file_filter(file):
                    dynamic_files.add(os.path.join(method_dir, file))

    for scan_dir in scan_dirs:
        for root, _, files in os.walk(scan_dir):
            for file in sorted(files):
                if not file.endswith('.py') or file.startswith('__'):
                    continue

                module_path = os.path.join(root, file)
                
                # Skip dynamic method files in the main loop; they will be documented under their respective classes
                if module_path in dynamic_files:
                    continue

                relative_path = os.path.relpath(module_path, package_root)
                module_name = os.path.splitext(relative_path.replace(os.sep, '.'))[0]

                try:
                    module = importlib.import_module(module_name)
                    display_path = os.path.relpath(module_path, package_root)
                except Exception as e:
                    print(f"Warning: Could not import module {module_name}. Error: {e}. Skipping.")
                    continue

                docs += f"## Module: `{display_path}`\n\n"

                # Document functions
                for name, obj in inspect.getmembers(module, inspect.isfunction):
                    if obj.__module__ == module.__name__:
                        signature = inspect.signature(obj)
                        docstring = inspect.getdoc(obj) or "No docstring available."
                        docs += f"### `def {name}{signature}`\n"
                        docs += f"> {docstring}\n\n"

                # Document classes
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if obj.__module__ == module.__name__:
                        docs += f"### `class {name}`\n"
                        docstring = inspect.getdoc(obj) or "No docstring available."
                        docs += f"> {docstring}\n\n"

                        # Document static methods within the class
                        for method_name, method_obj in inspect.getmembers(obj, inspect.isfunction):
                            if not method_name.startswith('_'):
                                signature = inspect.signature(method_obj)
                                method_doc = inspect.getdoc(method_obj) or "No docstring available."
                                docs += f"#### `def {method_name}{signature}`\n"
                                docs += f"> {method_doc}\n\n"
                        
                        # Document dynamically loaded methods
                        if name in DYNAMIC_METHOD_DIRS:
                            method_dir, file_filter = DYNAMIC_METHOD_DIRS[name]
                            if os.path.isdir(method_dir):
                                for method_file in sorted(os.listdir(method_dir)):
                                    if method_file.endswith('.py') and file_filter(method_file):
                                        dyn_module_path = os.path.join(method_dir, method_file)
                                        dyn_relative_path = os.path.relpath(dyn_module_path, package_root)
                                        dyn_module_name = os.path.splitext(dyn_relative_path.replace(os.sep, '.'))[0]
                                        
                                        try:
                                            dyn_module = importlib.import_module(dyn_module_name)
                                            for dyn_method_name, dyn_method_obj in inspect.getmembers(dyn_module, inspect.isfunction):
                                                if dyn_method_obj.__module__ == dyn_module.__name__:
                                                    actual_method_name = os.path.splitext(method_file)[0]
                                                    signature = inspect.signature(dyn_method_obj)
                                                    method_doc = inspect.getdoc(dyn_method_obj) or "No docstring available."
                                                    docs += f"#### `def {actual_method_name}{signature}` (Dynamically Loaded)\n"
                                                    docs += f"> {method_doc}\n\n"
                                        except Exception as e:
                                            print(f"Warning: Could not import dynamic module {dyn_module_name}. Error: {e}. Skipping.")
                docs += "---\n"

    with open(output_file, 'w') as f:
        f.write(docs)
    print(f"API documentation successfully generated at {output_file}")

if __name__ == "__main__":
    package_root_dir = "src"
    # The main directory to scan. The script will intelligently handle dynamic method dirs.
    scan_target_dirs = ["src/dw6"]
    output_markdown_file = "docs/API_REFERENCE.md"
    generate_api_docs(package_root_dir, scan_target_dirs, output_markdown_file)
