#!/bin/python3

import os

files = [f'{i}.md' for i in range(0, 57)]

with open('all.md', 'w') as all_md:
    all_md.write('\\pagebreak')
    for file in files:
        try:
            with open(file, 'r') as f:
                if os.system(
                    f'pandoc {file} -o {file}.pdf '
                    '-t latex --pdf-engine=xelatex '
                    '-V mainfont="Liberation Serif" -V fontsize=12pt '
                ) != 0:
                    raise ValueError()
                os.remove(f'{file}.pdf')
                content = f.read()
            all_md.write(content)
            all_md.write('\n\n\\pagebreak\n\n')
        except ValueError:
            print(f"Error in {file}")
        except:
            pass

os.system(
    'pandoc all.md -o all.pdf '
    '-t latex --pdf-engine=xelatex '
    '-V mainfont="Liberation Serif" -V fontsize=12pt '
    '-V geometry:margin=1in '
    '--toc --toc-depth=1 --number-sections '
)

os.remove('all.md')

