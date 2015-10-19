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
        return open(srcfile).readlines()
    except IOError:
        print('Could not open', srcfile)
        return ''

def clean_imports(source):
    """ removes all additional module level imports"""
    previous_imports = []
    clean_lines = []
    for line in source:
        if line in previous_imports:
            continue
        if line.startswith("import") or line.startswith("from "):
            previous_imports.append(line)
        clean_lines.append(line)
    return clean_lines

def segment_line(name):
    return '\n#{:#^80}\n'.format(' {} '.format(name))

if __name__ == "__main__":
    source = load_source(TEMPLATE_FILE)
    source.append(segment_line('defaults'))
    source += load_source(os.path.join(THEMES_DIR, 'default.py'))
    source.append(segment_line('theme: ' + config.THEME))
    source += load_source(os.path.join(THEMES_DIR, config.THEME + '.py'))
    source.append(segment_line('SEGMENTS'))
    for segment in config.SEGMENTS:
        source.append(segment_line(segment))
        source += load_source(os.path.join(SEGMENTS_DIR, segment + '.py'))

    source.append(segment_line('write out'))
    source.append('sys.stdout.write(powerline.draw())\n')
    source = clean_imports(source)
    source = ''.join(source) + '\n\n'


    try:
        open(OUTPUT_FILE, 'w').write(source)
        st = os.stat(OUTPUT_FILE)
        os.chmod(OUTPUT_FILE, st.st_mode | stat.S_IEXEC)
        print(OUTPUT_FILE, 'saved successfully')
    except IOError:
        print('ERROR: Could not write to powerline-shell.py. Make sure it is writable')
        exit(1)
