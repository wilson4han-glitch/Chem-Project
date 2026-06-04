"""
Parse all Claude Code session JSONL files for this project into a clean transcript.md.
Extracts real user messages and assistant text responses, sorted chronologically.
"""

import json
import os
import re
from datetime import datetime, timezone

PROJECT_DIR = os.path.expanduser(
    '~/.claude/projects/-Users-WilsonHan-Desktop-Chem-Project'
)
OUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'transcript.md')

# Patterns that indicate a message is system noise, not a real user turn
COMMAND_RE = re.compile(r'<command-name>|<local-command|<command-message>|<system-reminder')


def extract_text(content):
    """Return plain text from a message's content field (str or list of blocks)."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get('type') == 'text':
                t = block.get('text', '').strip()
                if t:
                    parts.append(t)
        return '\n\n'.join(parts)
    return ''


def is_noise(text):
    """Return True if the text is a system injection or slash-command, not a real message."""
    if not text:
        return True
    if COMMAND_RE.search(text):
        return True
    return False


def load_session(path):
    """Load a JSONL session file and return a list of (timestamp, role, text) tuples."""
    turns = []
    with open(path, encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError:
                continue

            msg_type = obj.get('type')
            if msg_type not in ('user', 'assistant'):
                continue
            if obj.get('isMeta', False):
                continue
            if obj.get('isSidechain', False):
                continue

            msg = obj.get('message', {})
            role = msg.get('role', '')
            if role not in ('user', 'assistant'):
                continue

            text = extract_text(msg.get('content', ''))
            if is_noise(text):
                continue

            ts_str = obj.get('timestamp', '')
            try:
                ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                ts = datetime.min.replace(tzinfo=timezone.utc)

            turns.append((ts, role, text))

    return turns


def main():
    jsonl_files = sorted(
        f for f in os.listdir(PROJECT_DIR) if f.endswith('.jsonl')
    )

    all_turns = []
    for fname in jsonl_files:
        path = os.path.join(PROJECT_DIR, fname)
        turns = load_session(path)
        all_turns.extend(turns)

    # Sort all turns across all sessions by timestamp
    all_turns.sort(key=lambda t: t[0])

    # Deduplicate: consecutive identical (role, text) pairs sometimes appear due
    # to context compaction replaying messages.
    deduped = []
    prev = None
    for ts, role, text in all_turns:
        key = (role, text)
        if key != prev:
            deduped.append((ts, role, text))
            prev = key

    # Write transcript
    lines = [
        '# Project Transcript — AP Chemistry Electrochemistry Simulation\n',
        f'*Parsed from Claude Code session logs · {len(deduped)} exchanges · '
        f'Sessions: {len(jsonl_files)}*\n',
        '\n---\n',
    ]

    current_date = None
    for ts, role, text in deduped:
        date_str = ts.strftime('%Y-%m-%d')
        if date_str != current_date:
            current_date = date_str
            lines.append(f'\n## {ts.strftime("%B %d, %Y")}\n')

        time_str = ts.strftime('%H:%M')
        if role == 'user':
            lines.append(f'\n**User** _{time_str}_\n\n{text}\n')
        else:
            lines.append(f'\n**Claude** _{time_str}_\n\n{text}\n')

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'Wrote {len(deduped)} turns to {OUT_FILE}')


if __name__ == '__main__':
    main()
