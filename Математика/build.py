#!/bin/python3

import os
import subprocess

files = [f'{i}.md' for i in range(36, 52)]

with open('all.md', 'w') as all_md:
    all_md.write('\\pagebreak')
    for file in files:
        print(f'Checking {file}... ', end='')
        try:
            with open(file, 'r') as f:
                process = subprocess.run([
                    'pandoc', file, '-o', f'{file}.pdf',
                    '-t', 'latex', '--pdf-engine=xelatex',
                    '-V', "mainfont=Liberation Serif", '-V', 'fontsize=12pt'],
                    capture_output=True
                )
                
                if process.returncode:
                    print(f"Error")
                    for line in process.stderr.decode().splitlines():
                        print(f'    {line}')
                    raise ValueError()
                os.remove(f'{file}.pdf')
                content = f.read()
            all_md.write(content)
            all_md.write('\n\n\\pagebreak\n\n')
            print("Ok")
        except IOError:
            print("Not exists.")
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

