#!/usr/bin/env python3
"""
Add folder-based tags to all notes in 03 WIKI/.
For each note, adds a tag for each containing subfolder (below 03 WIKI/).
Tags are lowercase with hyphens replacing spaces.
"""

import os
import re
from pathlib import Path

VAULT_ROOT = Path("/Users/S.Parodi/Library/Mobile Documents/com~apple~CloudDocs/Obsidian/DataPlatform")
WIKI_ROOT = VAULT_ROOT / "03 WIKI"


def folder_to_tag(folder_name: str) -> str:
    """Convert a folder name to a tag: lowercase, spaces → hyphens."""
    return folder_name.lower().replace(" ", "-")


def parse_frontmatter(content: str):
    """Return (frontmatter_str, body_str) or (None, content) if no frontmatter."""
    if not content.startswith("---"):
        return None, content
    end = content.find("\n---", 3)
    if end == -1:
        return None, content
    fm = content[3:end].strip()
    body = content[end + 4:]
    return fm, body


def get_tags_from_frontmatter(fm: str) -> list[str]:
    """Extract tags list from frontmatter string."""
    # Match: tags:\n  - tag1\n  - tag2
    # or: tags: [tag1, tag2]
    # or: tags: []
    block_match = re.search(r'^tags:\s*\n((?:\s+-\s+.+\n?)*)', fm, re.MULTILINE)
    if block_match:
        tags_block = block_match.group(1)
        return re.findall(r'^\s+-\s+(.+)', tags_block, re.MULTILINE)

    inline_match = re.search(r'^tags:\s*\[([^\]]*)\]', fm, re.MULTILINE)
    if inline_match:
        content = inline_match.group(1).strip()
        if not content:
            return []
        return [t.strip().strip('"\'') for t in content.split(',')]

    return []


def set_tags_in_frontmatter(fm: str, new_tags: list[str]) -> str:
    """Replace or insert the tags field in the frontmatter string."""
    tags_yaml = "tags:\n" + "".join(f"  - {t}\n" for t in new_tags)

    # Replace existing block tags
    block_pattern = re.compile(r'^tags:\s*\n(?:\s+-\s+.+\n?)*', re.MULTILINE)
    if block_pattern.search(fm):
        return block_pattern.sub(tags_yaml, fm)

    # Replace existing inline tags
    inline_pattern = re.compile(r'^tags:\s*\[[^\]]*\]', re.MULTILINE)
    if inline_pattern.search(fm):
        return inline_pattern.sub(tags_yaml.rstrip('\n'), fm)

    # No tags field: append it
    return fm + "\n" + tags_yaml.rstrip('\n')


def process_file(filepath: Path) -> tuple[bool, str]:
    """Process one file. Returns (modified, message)."""
    rel = filepath.relative_to(WIKI_ROOT)
    parts = rel.parts[:-1]  # folders between WIKI_ROOT and file

    if not parts:
        return False, f"SKIP (root): {rel}"

    folder_tags = [folder_to_tag(p) for p in parts]

    content = filepath.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    if fm is None:
        return False, f"NO FRONTMATTER: {rel}"

    existing_tags = get_tags_from_frontmatter(fm)
    existing_lower = [t.lower() for t in existing_tags]

    tags_to_add = [t for t in folder_tags if t not in existing_lower]

    if not tags_to_add:
        return False, f"OK (no change): {rel}"

    new_tags = existing_tags + tags_to_add
    new_fm = set_tags_in_frontmatter(fm, new_tags)
    new_content = f"---\n{new_fm}\n---{body}"
    filepath.write_text(new_content, encoding="utf-8")

    return True, f"UPDATED (+{tags_to_add}): {rel}"


def main():
    modified = 0
    skipped = 0
    errors = 0

    for md_file in sorted(WIKI_ROOT.rglob("*.md")):
        try:
            changed, msg = process_file(md_file)
            print(msg)
            if changed:
                modified += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"ERROR: {md_file.relative_to(WIKI_ROOT)}: {e}")
            errors += 1

    print(f"\n--- Summary ---")
    print(f"Modified: {modified}")
    print(f"Skipped/unchanged: {skipped}")
    print(f"Errors: {errors}")


if __name__ == "__main__":
    main()
