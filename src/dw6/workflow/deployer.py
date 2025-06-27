import os
import importlib
import inspect

class DeployerStage:
    """Handles the deployment of the project by dynamically loading methods."""
    pass

# Dynamically load and attach methods
def _attach_methods():
    # The class to which methods will be attached.
    cls = DeployerStage
    
    # Path to the directory containing method implementations.
    dp_path = os.path.join(os.path.dirname(__file__), 'dp')
    
    # Iterate through each file in the 'dp' directory.
    for filename in os.listdir(dp_path):
        # Process only Python files, excluding the __init__.py file.
        if filename.endswith('.py') and filename != '__init__.py':
            # Construct the module name from the filename.
            module_name = f"dw6.workflow.dp.{filename[:-3]}"
            
            try:
                # Import the module dynamically.
                module = importlib.import_module(module_name)
                
                # Iterate through the members of the imported module.
                for name, func in inspect.getmembers(module, inspect.isfunction):
                    # Attach the function to the class.
                    setattr(cls, name, func)
            except ImportError as e:
                # Handle any import errors, e.g., by logging.
                print(f"Error importing {module_name}: {e}")

# Run the dynamic attachment process.
_attach_methods()