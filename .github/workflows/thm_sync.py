import re
import json
import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup

PROFILE = 'https://tryhackme.com/p/william.l.munoz'
REPO_ROOT = Path(__file__).resolve().parents[2]
README = REPO_ROOT / 'README.md'
STATE = REPO_ROOT / '.thm_state.json'


def fetch_profile_html():
    r = requests.get(PROFILE, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
    r.raise_for_status()
    return r.text


def parse_badges(html):
    # Heuristic: badge names often appear as text like 'cat linux.txt' or inside alt/title attributes
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(" ")
    # Very loose: collect known badge-like tokens around 'badge' or typical badge strings
    candidates = set()
    for m in re.finditer(r"(?i)(cat linux\.txt|linux|windows|principles|web|networking|crypto|forensics|pwn|owasp|advent|presecurity)\b[\w .+\-]*", text):
        candidates.add(m.group(0).strip())
    # Always include explicit 'cat linux.txt' if present
    if 'cat linux.txt' in text:
        candidates.add('cat linux.txt')
    # Clean up
    cleaned = sorted({c for c in candidates if 3 <= len(c) <= 60})
    return cleaned


def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text())
        except Exception:
            return {"badges": []}
    return {"badges": []}


def save_state(state):
    STATE.write_text(json.dumps(state, indent=2))


def update_readme(badges):
    md = README.read_text()
    # Ensure Badges section exists
    if '## Badges' not in md:
        md += '\n\n## Badges\n'
    lines = md.splitlines()
    # Build a set of existing badge lines
    existing = set()
    for line in lines:
        if line.strip().startswith('- '):
            existing.add(line.strip().lstrip('- ').strip())
    # Append any new badges with link to profile
    new_lines = []
    for b in badges:
        entry = f"{b} — See profile"
        if not any(b in ex for ex in existing):
            new_lines.append(f"- {b}  ")
            new_lines.append(f"  View badge: {PROFILE}")
    if new_lines:
        # Insert under '## Badges' after that header
        out = []
        inserted = False
        for i, line in enumerate(lines):
            out.append(line)
            if not inserted and line.strip() == '## Badges':
                out.extend(new_lines)
                inserted = True
        if not inserted:
            out.append('## Badges')
            out.extend(new_lines)
        new_md = '\n'.join(out) + '\n'
        README.write_text(new_md)
        return True
    return False


def main():
    html = fetch_profile_html()
    badges = parse_badges(html)
    state = load_state()
    known = set(state.get('badges', []))
    new_badges = [b for b in badges if b not in known]
    changed = False
    if new_badges:
        state['badges'] = sorted(known | set(new_badges))
        save_state(state)
        changed |= update_readme(new_badges)
    if not changed:
        print('No updates found')

if __name__ == '__main__':
    main()
