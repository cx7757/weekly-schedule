#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键完成：注入笔记 + git add + commit + push"""
import json
import re
import subprocess
import sys
import os

HTML_PATH = "index.html"
INPUT_JSON = "notes_daily_20260510.json"
COMMIT_MSG = "docs: daily notes update 2026-05-10 +13"

def run(cmd, check=True):
    print(f">>> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.stdout:
        print(result.stdout[:500])
    if result.stderr:
        print("STDERR:", result.stderr[:500])
    if check and result.returncode != 0:
        print(f"ERROR: command failed with return code {result.returncode}")
        sys.exit(1)
    return result

def inject():
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        new_notes = json.load(f)

    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'(const NOTES_DB\s*=\s*)(\{[\s\S]*?\})\s*;', content)
    if not match:
        print("ERROR: NOTES_DB not found")
        sys.exit(1)

    notes_db = json.loads(match.group(2))

    added = 0
    skipped = 0
    for note in new_notes:
        cat = note.get('category', '')
        subcat = note.get('subcategory', '')
        text = note.get('text', '').strip()
        if not cat or not subcat or not text:
            continue
        if cat not in notes_db:
            notes_db[cat] = {}
        if subcat not in notes_db[cat]:
            notes_db[cat][subcat] = []
        existing = {item.get('t', '') for item in notes_db[cat][subcat]}
        if text in existing:
            skipped += 1
            continue
        notes_db[cat][subcat].append({"t": text})
        added += 1

    if added == 0:
        print(f"No new notes to inject (skipped {skipped} duplicates)")
        return False

    new_str = json.dumps(notes_db, ensure_ascii=False, indent=2)
    new_content = content[:match.start(2)] + new_str + content[match.end(2):]
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Injected {added} new notes, skipped {skipped} duplicates")
    return True

def git_commit_push():
    run("git add index.html", check=False)
    result = run(f'git commit -m "{COMMIT_MSG}"', check=False)
    if result.returncode != 0:
        print("Commit failed, checking status...")
        run("git status --porcelain", check=False)
        return False
    print("Commit succeeded!")
    result = run("git push origin main", check=False)
    if result.returncode != 0:
        print("Push failed (network issue?), giving up as required")
        return False
    print("Push succeeded!")
    return True

if __name__ == '__main__':
    print("=== Step 1: Inject notes ===")
    injected = inject()
    if not injected:
        print("No injection needed, checking if commit/push still needed...")
    print("\n=== Step 2: Git commit & push ===")
    git_commit_push()
    print("=== Done ===")
