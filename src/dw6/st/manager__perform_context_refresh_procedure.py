import os

def _perform_context_refresh_procedure(self):
    """Reads all critical project documents to rebuild context."""
    print("--- Governor: Reading all critical project documents... ---")
    critical_docs = [
        "docs/PROJECT_REQUIREMENTS.md",
        "docs/AI_PROTOCOL_TUTORIAL.md",
        "docs/protocols/DW8_PROTOCOL_DEFINITION.md",
        "README.md"
    ]
    
    restored_context = ""
    for doc_path in critical_docs:
        if os.path.exists(doc_path):
            with open(doc_path, "r") as f:
                content = f.read()
                restored_context += f"\n\n--- Contents of {doc_path} ---\n{content}"
    
    # Store the restored context in a temporary state variable for the report
    self.state.set("__temp_restored_context", restored_context)
