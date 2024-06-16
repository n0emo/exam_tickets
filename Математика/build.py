#!/bin/python3

import os
import subprocess
import sys
import shutil

files = [f'{str(i).zfill(2)}.md' for i in range(8, 9)]

def compile_pdf(input_file, output_file):
    return subprocess.run([
        'pandoc', input_file, '-o', f'{output_file}.pdf',
        '-t', 'latex', '--pdf-engine=xelatex',
        '-V', "mainfont=Times New Roman", '-V', 'fontsize=12pt',
        '-V', 'geometry:margin=1in',
        '--toc', '--toc-depth=1', '--number-sections',
        '-H', 'packages.tex'
        ], capture_output=True
    )

if not os.path.exists('build'):
    os.makedirs('build')

shutil.copytree('attachments', os.path.join('build', 'attachments'), dirs_exist_ok=True)

success_count = 0
fail_count = 0
not_exists_count = 0
with_warning_count = 0

all_md_path = os.path.join('build', 'all.md')
with open(all_md_path, 'w') as all_md:
    all_md.write('\\pagebreak\n\n')

    for file in files:
        print(f'Checking {file}... ', end='')

        warnings = []
        try:
            content: str
            with open(file, 'r') as f:
                content = f.read()

            process = compile_pdf(file, os.path.join('build', file))               
            if process.returncode:
                print(f"Error")
                for line in process.stderr.decode().splitlines():
                    print(f'    {line}')
                raise ValueError()

            all_md.write(content)
            all_md.write('\n\n\\pagebreak\n\n')

            warnings = process.stderr.decode().splitlines()
            
        except IOError:
            not_exists_count += 1
            print("Not exists.")
        except KeyboardInterrupt:
            print('\nKeyboard Interrupt')
            sys.exit(0)
        except:
            fail_count += 1
        else:
            if len(warnings):
                with_warning_count += 1
                print(f"Ok (with {len(warnings)} warnings)")
                if '-v' in sys.argv:
                    for line in warnings: 
                        print(f'    {line}')
            else:
                success_count += 1
                print("Ok")

print(f'All files checked:')
print(f'    Succeeded:     {success_count}')
print(f'    With warnings: {with_warning_count}')
print(f'    Failed:        {fail_count}')
print(f'    Not exists:    {not_exists_count}')
print('')
print(f'    Total:         {success_count + with_warning_count + fail_count + not_exists_count}')
print("Compiling PDF...")
proccess = compile_pdf(all_md_path, all_md_path)

if proccess.returncode:
    print("Error compiling final PDF:")
    for line in proccess.stderr.decode().splitlines():
        print(f'    {line}')
else:
    print("Successfully compiled PDF.")

