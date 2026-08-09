import subprocess
import os

subprocess.run(['git', 'checkout', 'HEAD', '--', 'src/bugpilot/utils/changelog.py'])

cl = 'src/bugpilot/utils/changelog.py'
with open(cl, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
for i, line in enumerate(lines):
    if 'CHANGELOG.md' in line and 'Path(__file__)' in line:
        lines[i] = '    (Path(__file__).parent.parent.parent.parent / "CHANGELOG.md").read_text(encoding="utf-8")'

with open(cl, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
