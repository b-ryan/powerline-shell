#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

class Powerline:
    separator = '⮀'
    separator_thin='⮁'
    LSQESCRSQ = '\\[\\e%s\\]'
    clear_fg = LSQESCRSQ % '[38;0m'
    clear_bg = LSQESCRSQ % '[48;0m'
    reset = LSQESCRSQ % '[0m'

    def __init__(self):
        self.segments = []

    def append(self, content, fg, bg, separator=None, separator_fg=None):
      if separator == None:
        separator = self.separator
      if separator_fg == None:
        separator_fg = bg
      segment = {
          'content': content,
          'fg': fg,
          'bg': bg,
          'separator': separator,
          'separator_fg': separator_fg
          }
      self.segments.append(segment)

    def color(self, prefix, code):
        return self.LSQESCRSQ % ('[%s;5;%sm' % (prefix, code))

    def fgcolor(self, code):
        return self.color('38', code)

    def bgcolor(self, code):
        return self.color('48', code)

    def draw(self):
        line = ''.join(''.join((self.fgcolor(s['fg']), 
                                self.bgcolor(s['bg']),
                                s['content'],
                                self.fgcolor(s['separator_fg']), 
                                self.bgcolor(self.segments[i+1]['bg']), 
                                s['separator']))
                         for i, s in enumerate(self.segments[:-1]))
        
        s = self.segments[-1]
        return ''.join([line,
                        self.fgcolor(s['fg']), 
                        self.bgcolor(s['bg']), 
                        s['content'],
                        self.reset, 
                        self.fgcolor(s['separator_fg']), 
                        s['separator'], 
                        self.reset])

def is_git_clean():
    # [[ $(git status 2> /dev/null | tail -n1) != "nothing to commit (working directory clean)" ]] && echo "*"
    try:
        output = os.popen('git status 2> /dev/null | tail -n1 | grep "nothing to commit (working directory clean)" ').read()
        return len(output) > 0
    except subprocess.CalledProcessError:
        return 0

def add_git_segment(powerline):
    green = 148
    red = 161
    try:
        #cmd = "git branch 2> /dev/null | grep -e '\\*'"
        p1 = subprocess.Popen(['git', 'branch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(['grep', '-e', '\\*'], stdin=p1.stdout, stdout=subprocess.PIPE)
        output = p2.communicate()[0].strip()
        if len(output) > 0:
          branch = output.rstrip()[2:]
          bg = red
          fg = 15
          if is_git_clean():
              bg = green
              fg = 0
          powerline.append(' %s ' % branch, fg, bg)
    # if git or grep is not installed on the machine
    except OSError:
      pass
    except subprocess.CalledProcessError:
      pass

def add_svn_segment(powerline):
    '''svn info:
        First column: Says if item was added, deleted, or otherwise changed
        ' ' no modifications
        'A' Added
        'C' Conflicted
        'D' Deleted
        'I' Ignored
        'M' Modified
        'R' Replaced
        'X' an unversioned directory created by an externals definition
        '?' item is not under version control
        '!' item is missing (removed by non-svn command) or incomplete
         '~' versioned item obstructed by some item of a different kind
    '''
    #TODO: Color segment based on above status codes
    try:
        #cmd = '"svn status | grep -c "^[ACDIMRX\\!\\~]"'
        p1 = subprocess.Popen(['svn', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(['grep', '-c', '^[ACDIMRX\\!\\~]'], stdin=p1.stdout, stdout=subprocess.PIPE)
        output = p2.communicate()[0].strip()
        if len(output) > 0 and int(output) > 0:
          changes = output.strip()
          powerline.append(' %s ' % changes, 22, 148)
    # if svn or grep is not installed on the machine
    except OSError:
      pass
    except subprocess.CalledProcessError:
      pass

# Show working directory with fancy separators
def add_cwd_segment(powerline):
    #powerline.append(' \\w ', 15, 237)
    home = os.getenv('HOME')
    cwd = os.getenv('PWD')

    if cwd.find(home) == 0:
      cwd = cwd.replace(home, '~', 1)

    if cwd[0] == '/':
      cwd = cwd[1:]

    names = cwd.split('/')
    for n in names[:-1]:
      powerline.append(' %s ' % n, 250, 237, Powerline.separator_thin, 244)
    powerline.append(' %s ' % names[-1], 254, 237)

def add_root_indicator(powerline, error):
    bg = 236
    fg = 15
    if int(error) != 0:
        fg = 15
        bg = 161
    powerline.append(' \\$ ', fg, bg)

if __name__ == '__main__':
    p = Powerline()
    p.append(' \\u ', 250, 240)
    p.append(' \\h ', 250, 238)
    add_cwd_segment(p)
    add_git_segment(p)
    add_svn_segment(p)
    add_root_indicator(p, sys.argv[1] if len(sys.argv) > 1 else 0)
    sys.stdout.write(p.draw())
