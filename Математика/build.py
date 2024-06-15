#!/bin/python3

import os

files = [f'{i}.md' for i in range(42, 45)]

with open('all.md', 'w') as all_md:
    all_md.write('\\pagebreak')
    for file in files:
        with open(file, 'r') as f:
            content = f.read()
        all_md.write(content)
        all_md.write('\n\\pagebreak\n')

os.system(
    'pandoc -t latex -o all.pdf --pdf-engine=xelatex '
    'all.md -V mainfont="Liberation Serif" '
    '--toc --toc-depth=1 --number-sections'
)

os.remove('all.md')

