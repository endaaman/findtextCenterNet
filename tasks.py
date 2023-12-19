import os
import re
from glob import glob
from tqdm import tqdm
import invoke


@invoke.task
def convert(c):
    for pdf in sorted(glob('*.pdf')):
        name = os.path.splitext(pdf)[0]
        d = f'/tmp/png/{name}'
        os.makedirs(d, exist_ok=True)
        cmd = f'pdftoppm -png {pdf} image {d}'
        print(cmd)
        # invoke.run(cmd)
        print('done')
        break

def num_to_page(num):
    if num <= 875:
        return num - 26
    return num - 25

@invoke.task
def geka(c):

    dest = 'tmp/geka.txt'

    with open(dest, 'w') as f:
        f.write('')

    for path in tqdm(sorted(glob('tmp/外科病理/image-*.png'))):
        # filename = os.path.splitext(os.path.basename(path))[0]
        # print(filename)
        num = int(re.match(r'^.*/image-(\d\d\d\d)\.png$', path)[1])
        page = num_to_page(num)
        with open(dest, 'a') as f:
            f.write(f'\n\n<<PAGE: {page}>>\n\n')
        cmd = f'./test_image2.py {path} {dest}'
        c.run(cmd, hide=True)
