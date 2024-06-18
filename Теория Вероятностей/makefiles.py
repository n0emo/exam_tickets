import os


count = 0

with open('Билеты.md', 'r') as f:
    content = [
        ' '.join(line.strip().split()[4::])
        for line in f.readlines() 
        if line.startswith('- [ ] ')
    ]


for index, line in enumerate(content):
    filename = str(index + 1).zfill(2) + '.md'
    with open(filename, 'w') as f:
        f.write('# ')
        f.write(line)
        f.write('\n\n')

