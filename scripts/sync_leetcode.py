#!/usr/bin/env python3
"""Generate MkDocs pages from Coding-Questions-Solutions/my-solutions."""
from pathlib import Path
import re
import shutil
import urllib.parse

SOURCE = Path("leetcode-source/my-solutions")
OUTPUT = Path("docs/learning/dsa/leetcode")
REPO_URL = "https://github.com/ashishpatidar123/Coding-Questions-Solutions"
BRANCH = "main"

def clean_title(folder: str) -> str:
    m = re.match(r"^(\d+)-(.+)$", folder)
    if not m:
        return folder.replace("-", " ").title()
    return f"{int(m.group(1))}. {m.group(2).replace('-', ' ').title()}"

def rewrite_readme_links(text: str, source_readme: Path) -> str:
    # Preserve external URLs; make relative paths link to source GitHub files.
    base = f"{REPO_URL}/blob/{BRANCH}/{urllib.parse.quote(source_readme.as_posix(), safe='/')}"
    def repl(match):
        label, target = match.group(1), match.group(2).strip()
        if not target or target.startswith(("http://", "https://", "#", "mailto:")):
            return match.group(0)
        path, sep, anchor = target.partition("#")
        resolved = (source_readme.parent / path).as_posix() if path else source_readme.as_posix()
        url = f"{REPO_URL}/blob/{BRANCH}/{urllib.parse.quote(resolved, safe='/')}"
        if sep:
            url += "#" + anchor
        return f"[{label}]({url})"
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)
    return text

def main():
    if not SOURCE.exists():
        raise SystemExit(f"Source folder not found: {SOURCE}")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    # Remove old generated problem pages only; leave unrelated files alone.
    problems_dir = OUTPUT / "problems"
    if problems_dir.exists():
        shutil.rmtree(problems_dir)
    problems_dir.mkdir(parents=True)

    groups = {}
    all_items = []
    for difficulty in ("Easy", "Medium", "Hard"):
        folder = SOURCE / difficulty
        entries = []
        if folder.exists():
            for problem in sorted(p for p in folder.iterdir() if p.is_dir()):
                readme = problem / "README.md"
                cpp_files = sorted(problem.glob("*.cpp"))
                if not readme.exists() and not cpp_files:
                    continue
                slug = problem.name
                title = clean_title(slug)
                page = problems_dir / f"{slug}.md"
                statement = readme.read_text(encoding="utf-8", errors="replace") if readme.exists() else "_Problem statement README not present._"
                statement = rewrite_readme_links(statement, readme) if readme.exists() else statement
                source_base = f"{REPO_URL}/tree/{BRANCH}/my-solutions/{difficulty}/{slug}"
                chunks = [
                    f"# {title}",
                    "",
                    f"**Difficulty:** {difficulty}  ",
                    f"**Source folder:** [View on GitHub]({source_base})",
                    "",
                    "## Problem",
                    "",
                    statement.strip(),
                    "",
                    "## My C++ Submissions",
                    "",
                ]
                if cpp_files:
                    for cpp in cpp_files:
                        code = cpp.read_text(encoding="utf-8", errors="replace")
                        source_url = f"{source_base}/{urllib.parse.quote(cpp.name)}"
                        chunks += [f"### `{cpp.name}`", "", f"[View source on GitHub]({source_url})", "", "```cpp", code.rstrip(), "```", ""]
                else:
                    chunks += ["_No C++ solution file found._", ""]
                chunks += ["---", "", f"[← Back to {difficulty}]({difficulty.lower()}.md) · [All problems](index.md)", ""]
                page.write_text("\n".join(chunks), encoding="utf-8")
                entry = (slug, title)
                entries.append(entry)
                all_items.append((difficulty, slug, title))
        groups[difficulty] = entries

    def listing(title, entries, description=""):
        out = [f"# {title}", ""]
        if description:
            out += [description, ""]
        out += [f"**Total: {len(entries)} problems**", ""]
        if entries:
            out += ["| Problem |", "|---|"]
            out += [f"| [{name}](problems/{slug}.md) |" for slug, name in entries]
        else:
            out += ["_No problems found._"]
        out += [""]
        return "\n".join(out)

    OUTPUT.joinpath("easy.md").write_text(listing("Easy Problems", groups["Easy"]), encoding="utf-8")
    OUTPUT.joinpath("medium.md").write_text(listing("Medium Problems", groups["Medium"]), encoding="utf-8")
    OUTPUT.joinpath("hard.md").write_text(listing("Hard Problems", groups["Hard"]), encoding="utf-8")

    index = [
        "# LeetCode Solutions",
        "",
        "Browse the problem statements and C++ submissions synced from my [Coding-Questions-Solutions repository](https://github.com/ashishpatidar123/Coding-Questions-Solutions).",
        "",
        f"**{len(all_items)} problems synced**",
        "",
        "| Difficulty | Count |",
        "|---|---:|",
    ]
    for d in ("Easy", "Medium", "Hard"):
        index.append(f"| [{d}]({d.lower()}.md) | {len(groups[d])} |")
    index += ["", "## All Problems", "", "| Difficulty | Problem |", "|---|---|"]
    for d, slug, title in sorted(all_items, key=lambda x: (x[0], x[1])):
        index.append(f"| {d} | [{title}](problems/{slug}.md) |")
    index += ["", "_Pages are generated automatically. Run the **Sync LeetCode** workflow to refresh._", ""]
    OUTPUT.joinpath("index.md").write_text("\n".join(index), encoding="utf-8")
    print(f"Generated {len(all_items)} problem pages in {OUTPUT}")

if __name__ == "__main__":
    main()
