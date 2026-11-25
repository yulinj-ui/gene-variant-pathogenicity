#!/usr/bin/env python3
"""Standard-library checks for this package's restricted YAML scalar format and local links.
Not the official skill-creator validator or a general YAML parser.
"""
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]

# Provenance snapshots (upstream archives, old `original/` files) are kept verbatim for audit:
# they are not live documentation, so their links are not required to resolve.
def is_archive(path):
    return any(part == 'original' or part.startswith('upstream-') for part in path.parts)

text = (root/'SKILL.md').read_text()
assert text.startswith('---\n')
front, body = text[4:].split('\n---\n',1)
assert re.search(r'^name: gene-variant-pathogenicity$', front, re.M)
assert re.search(r'^description: .{1,1024}$', front, re.M)
# Version is read from the package itself instead of being pinned here: a hardcoded
# version made every upgrade fail this validator before any real check ran.
version_match = re.search(r'^metadata:\n  version: (\S+)$', front, re.M)
assert version_match, 'metadata.version missing'
version = version_match.group(1)
assert re.fullmatch(r'\d+\.\d+\.\d+(?:-[A-Za-z0-9.]+)?', version), version
assert [l.split(':')[0] for l in front.splitlines() if not l.startswith(' ')] == ['name','description','metadata']
assert '<' not in front and '>' not in front
entries = [p for p in root.rglob('SKILL.md') if not is_archive(p.relative_to(root))]
assert len(entries) == 1, entries
for path in root.rglob('*.md'):
    if is_archive(path.relative_to(root)): continue
    content=path.read_text()
    assert content.count('```') % 2 == 0, str(path)
    for link in re.findall(r'\]\(([^)]+)\)',content):
        if '://' in link or link.startswith('#') or link == '{相对路径}': continue
        assert (path.parent/link.split('#')[0]).exists(), (path,link)
for item in json.loads((root/'review/source-manifest.json').read_text()):
    assert hashlib.sha256((root/item['file']).read_bytes()).hexdigest() == item['sha256']
print(f'PASS: local package scalar frontmatter (version {version}), references, fences, single entrypoint and original hashes')
print('This is the bundled local validator; see the separate official validator log for its result.')
