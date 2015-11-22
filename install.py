#!/usr/bin/env python2
from __future__ import print_function
import os
import stat

try:
    import config
except ImportError:
    print('Created personal config.py for your customizations')
    import shutil
    shutil.copyfile('config.py.dist', 'config.py')
    import config

TEMPLATE_FILE = 'powerline_shell_base.py'
OUTPUT_FILE = 'powerline-shell.py'
SEGMENTS_DIR = 'segments'
THEMES_DIR = 'themes'

def load_source(srcfile):
    try:
        return ''.join(open(srcfile).readlines()) + '\n\n'
    except IOError:
        print('Could not open', srcfile)
        return ''

if __name__ == "__main__":
    source = load_source(TEMPLATE_FILE)
    source += load_source(os.path.join(THEMES_DIR, 'default.py'))

    if config.THEME != 'default':
        source += load_source(os.path.join(THEMES_DIR, config.THEME + '.py'))

    for segment in config.SEGMENTS:
        source += load_source(os.path.join(SEGMENTS_DIR, segment + '.py'))

    source += 'sys.stdout.write(powerline.draw())\n'

    try:
        open(OUTPUT_FILE, 'w').write(source)
        st = os.stat(OUTPUT_FILE)
        os.chmod(OUTPUT_FILE, st.st_mode | stat.S_IEXEC)
        print(OUTPUT_FILE, 'saved successfully')
    except IOError:
        print('ERROR: Could not write to powerline-shell.py. Make sure it is writable')
        exit(1)
