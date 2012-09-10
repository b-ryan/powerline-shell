#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

class Powerline:
    separator = '⮀'
    separator_thin="⮁"
    ESC = '\e'
    LSQ = '\['
    RSQ = '\]'
    clear_fg = LSQ + ESC + '[38;0m' + RSQ
    clear_bg = LSQ + ESC + '[48;0m' + RSQ
    reset = LSQ + ESC + '[0m' + RSQ

    def __init__(self):
        self.segments = []

    def append(self, content, fg, bg, separator=None, separator_fg=None):
      if separator == None:
        separator = self.separator
      if separator_fg == None:
        separator_fg = bg
      segment = {
          'content': str(content),
          'fg': str(fg),
          'bg': str(bg),
          'separator': str(separator),
          'separator_fg': str(separator_fg)
          }
      self.segments.append(segment)

    def color(self, prefix, code):
        return self.LSQ + self.ESC + '[' + prefix + ';5;' + code + 'm' + self.RSQ

    def fgcolor(self, code):
        return self.color('38', code)

    def bgcolor(self, code):
        return self.color('48', code)

    def draw(self):
        i=0
        line=''
        while i < len(self.segments)-1:
            s = self.segments[i]
            ns = self.segments[i+1]
            line += self.fgcolor(s['fg']) + self.bgcolor(s['bg']) + s['content']
            line += self.fgcolor(s['separator_fg']) + self.bgcolor(ns['bg']) + s['separator']
            i += 1
        s = self.segments[i]
        line += self.fgcolor(s['fg']) + self.bgcolor(s['bg']) + s['content']
        line += self.reset + self.fgcolor(s['separator_fg']) + s['separator'] + self.reset
        return line

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
        #cmd = "git branch 2> /dev/null | grep -e '\*'"
        p1 = subprocess.Popen(['git', 'branch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(['grep', '-e', '\*'], stdin=p1.stdout, stdout=subprocess.PIPE)
        output = p2.communicate()[0].strip()
        if len(output) > 0:
          branch = output.rstrip()[2:]
          bg = red
          fg = 15
          if is_git_clean():
              bg = green
              fg = 0
          p.append(' ' + branch + ' ', fg, bg)
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
        #cmd = '"svn status | grep -c "^[ACDIMRX\!\~]"'
        p1 = subprocess.Popen(['svn', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(['grep', '-c', '^[ACDIMRX\!\~]'], stdin=p1.stdout, stdout=subprocess.PIPE)
        output = p2.communicate()[0].strip()
        if len(output) > 0 and int(output) > 0:
          changes = output.strip()
          p.append(' ' + changes + ' ', 22, 148)
    # if svn or grep is not installed on the machine
    except OSError:
      pass
    except subprocess.CalledProcessError:
      pass

# Show working directory with fancy separators
def add_cwd_segment(powerline):
    #p.append(' \w ', 15, 237)
    home = os.getenv('HOME')
    cwd = os.getenv('PWD')

    if cwd.find(home) == 0:
      cwd = cwd.replace(home, '~', 1)

    if cwd[0] == '/':
      cwd = cwd[1:]

    names = cwd.split('/')
    for n in names[:-1]:
      powerline.append(' ' + n + ' ', 250, 237, Powerline.separator_thin, 244)
    powerline.append(' ' + names[-1] + ' ', 254, 237)

def add_root_indicator(powerline, error):
    bg = 236
    fg = 15
    if int(error) != 0:
        fg = 15
        bg = 161
    p.append(' \$ ', fg, bg)

if __name__ == '__main__':
    p = Powerline()
    p.append(' \u ', 250, 240)
    p.append(' \h ', 250, 238)
    add_cwd_segment(p)
    add_git_segment(p)
    add_svn_segment(p)
    add_root_indicator(p, sys.argv[1] if len(sys.argv) > 1 else 0)
    print p.draw(),
