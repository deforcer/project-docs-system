#!/usr/bin/env python3
"""Offline package checks. No writes, credentials or external requests."""
import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


def check_links(root, boundary=None):
    errors = []
    for path in sorted(root.rglob('*.md')):
        text = path.read_text(encoding='utf-8')
        # Our documents use inline links; examples in fenced code aren't links.
        prose = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)
        for raw in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)', prose):
            target = raw.strip().strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith('#'):
                continue
            dest = (path.parent / unquote(parsed.path)).resolve()
            if boundary and not dest.is_relative_to(boundary.resolve()):
                errors.append(f'{path.relative_to(root)}: link escapes package: {target}')
            elif not dest.exists():
                errors.append(f'{path.relative_to(root)}: missing link target: {target}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill', type=Path, help='Check a standalone copied skill directory')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    skill = (args.skill or repo / 'skills/project-docs-system').resolve()
    required = ['SKILL.md', 'agents/openai.yaml', 'references/setup.md',
                'references/maintenance.md', 'references/methodology.md']
    required += [f'assets/templates/{name}.md' for name in
                 ['feature', 'decision', 'note', 'test-case', 'procedure', 'work-log', 'resume']]
    required += [f'assets/workspace/{name}.md' for name in
                 ['navigation', 'project', 'process', 'agent-instructions', 'init']]
    errors = [f'Missing {name}' for name in required if not (skill / name).is_file()]
    if errors:
        print('\n'.join(errors))
        return 1
    entry = (skill / 'SKILL.md').read_text(encoding='utf-8')
    front = re.match(r'\A---\n(.*?)\n---\n', entry, re.S)
    if not front or not re.search(r'^name: project-docs-system$', front.group(1), re.M):
        errors.append('Missing/incorrect skill name in frontmatter')
    if not front or not re.search(r'^description: \S.+$', front.group(1), re.M):
        errors.append('Missing single-line description')
    forbidden = re.compile(r'/Users/|/Volumes/|https?://[^/\s]+\.(?:internal|corp|local)\b|-----BEGIN [A-Z ]*PRIVATE KEY-----|glpat-[A-Za-z0-9_-]{10,}')
    for path in sorted(skill.rglob('*')):
        if path.is_symlink():
            errors.append(f'Symlink inside portable package: {path.relative_to(skill)}')
        elif path.is_file():
            text = path.read_text(encoding='utf-8')
            if forbidden.search(text):
                errors.append(f'Possible source-workspace data in {path.relative_to(skill)}')
            if '{{' in text and 'assets' not in path.relative_to(skill).parts:
                errors.append(f'Unfilled template outside assets: {path.relative_to(skill)}')
    errors += check_links(skill, boundary=skill)
    if args.skill is None:
        errors += check_links(repo)
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'PASS: {len(required)} required files; links, portability, source-data checks')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
