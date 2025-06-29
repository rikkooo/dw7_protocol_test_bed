# scripts/build_manual.py

import os
import re

# Note: This script is designed to be run from the project root directory.
# Example: python scripts/build_manual.py

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(PROJECT_ROOT, 'docs', 'AI_OPERATIONS_MANUAL.md')
OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'docs', 'AI_OPERATIONS_MANUAL.compiled.md')
CHAPTERS_DIR = os.path.join(PROJECT_ROOT, 'docs')

def main():
    """Reads the master index, finds all chapter files, and compiles them into a single file."""
    print("Starting manual compilation...")
    
    try:
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            index_content = f.read()
    except FileNotFoundError:
        print(f"ERROR: Master index file not found at {INDEX_PATH}")
        return

    # Use regex to find all markdown links pointing to the manual_chapters directory
    # This is more robust than simple line splitting.
    chapter_paths = re.findall(r'\((manual_chapters/.*?\.md)\)', index_content)

    if not chapter_paths:
        print("ERROR: No chapter files found in the master index.")
        return

    compiled_content = []
    for rel_path in chapter_paths:
        chapter_full_path = os.path.join(CHAPTERS_DIR, rel_path)
        try:
            with open(chapter_full_path, 'r', encoding='utf-8') as infile:
                # Add the chapter title from the filename as a header
                filename = os.path.basename(rel_path)
                title = os.path.splitext(filename)[0].replace('_', ' ').title()
                compiled_content.append(f"# Chapter: {title}\n\n")
                compiled_content.append(infile.read())
        except FileNotFoundError:
            print(f"WARNING: Chapter file not found, skipping: {chapter_full_path}")

    try:
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as outfile:
            # Join with a clear separator
            outfile.write('\n\n---\n\n'.join(compiled_content))
    except IOError as e:
        print(f"ERROR: Could not write to output file {OUTPUT_PATH}: {e}")
        return

    print(f"Successfully compiled {len(chapter_paths)} chapters into {os.path.basename(OUTPUT_PATH)}")

if __name__ == "__main__":
    main()
