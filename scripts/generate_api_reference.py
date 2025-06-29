import os
import sys
import inspect
import importlib

def generate_api_docs(package_root, scan_dir, output_file):
    """Inspects the source code and generates a Markdown API reference."""
    # Add the package root to the system path to allow for correct imports
    sys.path.insert(0, os.path.abspath(package_root))

    docs = "# DW8 Code Atlas (API Reference)\n\n"
    docs += "This document is the single source of truth for the DW8 project's API. It is auto-generated from the source code's docstrings.\n\n---\n"

    for root, _, files in os.walk(scan_dir):
        for file in sorted(files):
            if file.endswith('.py') and not file.startswith('__'):
                module_path = os.path.join(root, file)
                
                # Calculate the full module name relative to the package root
                relative_path = os.path.relpath(module_path, package_root)
                module_name = os.path.splitext(relative_path.replace(os.sep, '.'))[0]

                try:
                    module = importlib.import_module(module_name)
                    relative_path = os.path.relpath(module_path, os.path.dirname(scan_dir))
                except Exception as e:
                    print(f"Warning: Could not import module {module_name}. Error: {e}. Skipping.")
                    continue

                docs += f"## Module: `{relative_path}`\n\n"

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

                        # Document methods within the class
                        for method_name, method_obj in inspect.getmembers(obj, inspect.isfunction):
                            if not method_name.startswith('_'):
                                signature = inspect.signature(method_obj)
                                method_doc = inspect.getdoc(method_obj) or "No docstring available."
                                docs += f"#### `def {method_name}{signature}`\n"
                                docs += f"> {method_doc}\n\n"
                docs += "---\n"

    with open(output_file, 'w') as f:
        f.write(docs)
    print(f"API documentation successfully generated at {output_file}")

if __name__ == "__main__":
    # The root directory of our package(s)
    package_root_dir = "src"
    # The specific directory we want to scan for this project
    scan_target_dir = "src/dw6"
    output_markdown_file = "docs/API_REFERENCE.md"
    generate_api_docs(package_root_dir, scan_target_dir, output_markdown_file)
