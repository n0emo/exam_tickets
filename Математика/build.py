#!/bin/python3

import os
import subprocess
import sys
import shutil

files = [f'{str(i).zfill(2)}.md' for i in range(21, 31)]

header = """---
header-includes:
  - \\usepackage{cancel}
  - \\usepackage{amsmath}
  - \\usepackage{mathtools} 
---
""" 

def compile_pdf(input_file, output_file):
    return subprocess.run([
        'pandoc', input_file, '-o', f'{output_file}.pdf',
        '-t', 'latex', '--pdf-engine=xelatex',
        '-V', "mainfont=Liberation Serif", '-V', 'fontsize=12pt',
        '-V', 'geometry:margin=1in',
        '--toc', '--toc-depth=1', '--number-sections'
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
    all_md.write(header)
    all_md.write('\n\n')
    all_md.write('\\pagebreak')

    for file in files:
        print(f'Checking {file}... ', end='')
        try:
            content: str
            with open(file, 'r') as f:
                content = f.read()

            filename_for_check = os.path.join('build', file)
            with open(filename_for_check, 'w') as f_for_check:
                f_for_check.write(header)
                f_for_check.write('\n\n')
                f_for_check.write(content)

            process = compile_pdf(filename_for_check, filename_for_check)               
            if process.returncode:
                print(f"Error")
                for line in process.stderr.decode().splitlines():
                    print(f'    {line}')
                raise ValueError()

            all_md.write(content)
            all_md.write('\n\n\\pagebreak\n\n')

            warnings = process.stderr.decode().splitlines()
            
            if len(warnings):
                with_warning_count += 1
                print(f"Ok (with {len(warnings)} warnings)")
                if '-v' in sys.argv:
                    for line in warnings: 
                        print(f'    {line}')
            else:
                success_count += 1
                print("Ok")

        except IOError:
            not_exists_count += 1
            print("Not exists.")
        except KeyboardInterrupt:
            print('\nKeyboard Interrupt')
            sys.exit(0)
        except:
            fail_count += 1
            pass

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

