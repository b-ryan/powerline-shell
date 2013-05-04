import os

CONFIG_FILE = '.config'
TEMPLATE_FILE = 'powerline-shell.py.template'
OUTPUT_FILE = 'powerline-shell.py'
SEGMENTS_DIR = 'segments'

def load_source(srcfile):
    try:
        return ''.join(open(srcfile).readlines())
    except IOError:
        print 'Could not open ' + srcfile
        return ''

if __name__ == "__main__":
    source = load_source(TEMPLATE_FILE)
    source += '\n#--- Code inserted by configure.py ---'
    for line in open(CONFIG_FILE):
        line = line.strip()
        if len(line) > 0 and line[0] != '#':
            srcfile = os.path.join(SEGMENTS_DIR, line + '.py')
            source += '\n# ' + srcfile + '\n'
            source += load_source(srcfile)
            source += '\n# end of ' + srcfile + '\n'
    source += '\n#--- End of code inserted by configure.py ---'
    source += '\nsys.stdout.write(powerline.draw())\n'

    try:
        open(OUTPUT_FILE, 'w').write(source)
        print OUTPUT_FILE, 'saved successfully'
    except IOError:
        print 'ERROR: Could not write to powerline-shell.py. Make sure it is writable'
