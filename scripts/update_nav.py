from pathlib import Path

mkdocs_file = Path("mkdocs.yml")
content = mkdocs_file.read_text(encoding="utf-8")

nav_block = """      - LeetCode Solutions:
          - All Problems: learning/dsa/leetcode/index.md
          - Easy: learning/dsa/leetcode/easy.md
          - Medium: learning/dsa/leetcode/medium.md
          - Hard: learning/dsa/leetcode/hard.md
"""

marker = "      - DBMS:"

if "learning/dsa/leetcode/index.md" not in content:
    if marker not in content:
        raise RuntimeError("Could not find DBMS section in mkdocs.yml")

    content = content.replace(marker, nav_block + marker, 1)
    mkdocs_file.write_text(content, encoding="utf-8")

print("MkDocs navigation updated successfully.")
