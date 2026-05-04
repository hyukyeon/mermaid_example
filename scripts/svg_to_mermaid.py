#!/usr/bin/env python3
"""
svg_to_mermaid.py - Extract embedded Mermaid definitions from SVG files and write .mmd outputs.

Usage:
  scripts/svg_to_mermaid.py diagram.svg
  or
  python3 scripts/svg_to_mermaid.py diagram.svg

This performs a best-effort extraction: it searches <script type="text/plain" class="mermaid">, CDATA, <desc>, <metadata>, comments, and title tags, then looks for mermaid keywords.
"""

import sys
import re
import os

KEYWORDS = [
    'graph', 'flowchart', 'sequenceDiagram', 'gantt', 'classDiagram',
    'stateDiagram', 'erDiagram', 'pie', 'gitGraph', 'journey'
]

PATTERNS = [
    r'<script[^>]*type=["\']text/plain["\'][^>]*class=["\']?mermaid["\']?[^>]*>(.*?)</script>',
    r'<!\[CDATA\[(.*?)\]\]>',
    r'<desc>(.*?)</desc>',
    r'<metadata[^>]*>(.*?)</metadata>',
    r'<!--(.*?)-->',
    r'<title>(.*?)</title>',
]


def has_keyword(s: str) -> bool:
    ls = s.lower()
    return any(k.lower() in ls for k in KEYWORDS)


def extract_mermaid(text: str):
    candidates = []
    for p in PATTERNS:
        for m in re.findall(p, text, re.S | re.I):
            s = m.strip()
            if s:
                candidates.append(s)
    # Prefer candidate containing mermaid keywords
    good = [c for c in candidates if has_keyword(c)]
    if good:
        return max(good, key=len)
    # Fallback: find first appearance of a mermaid keyword and take until end
    m = re.search(r'((?:graph\s+[A-Za-z]+|flowchart|sequenceDiagram|gantt|classDiagram|stateDiagram|erDiagram|pie|gitGraph|journey)[\s\S]*)', text, re.I)
    if m:
        return m.group(1).strip()
    return None


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} file1.svg [file2.svg ...]", file=sys.stderr)
        sys.exit(2)
    found_any = False
    for path in sys.argv[1:]:
        if not os.path.isfile(path):
            print(f"File not found: {path}", file=sys.stderr)
            continue
        try:
            with open(path, 'r', encoding='utf-8') as f:
                txt = f.read()
        except Exception:
            with open(path, 'r', encoding='latin1') as f:
                txt = f.read()
        mermaid = extract_mermaid(txt)
        if mermaid:
            out = os.path.splitext(path)[0] + '.mmd'
            with open(out, 'w', encoding='utf-8') as of:
                of.write(mermaid.strip() + '\n')
            print(f"Extracted mermaid to {out}")
            found_any = True
        else:
            print(f"No mermaid found in {path}", file=sys.stderr)
    sys.exit(0 if found_any else 1)


if __name__ == '__main__':
    main()
