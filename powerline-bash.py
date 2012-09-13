#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

class Powerline:
    separator = '⮀'
    separator_thin='⮁'
    LSQESCRSQ = '\\[\\e%s\\]'
    reset = LSQESCRSQ % '[0m'

    def __init__(self):
        self.segments = []

    def color(self, prefix, code):
        return self.LSQESCRSQ % ('[%s;5;%sm' % (prefix, code))

    def fgcolor(self, code):
        return self.color('38', code)

    def bgcolor(self, code):
        return self.color('48', code)

    def append(self, segment):
        self.segments.append(segment)

    def draw(self):
        return (''.join((s[0].draw(self, s[1]) for s in zip(self.segments, self.segments[1:]+[None])))
            + self.reset)

class Segment:
    def __init__(self, content, fg, bg, separator=Powerline.separator, separator_fg=None):
        self.content = content
        self.fg = fg
        self.bg = bg
        self.separator = separator
        self.separator_fg = separator_fg or bg

    def draw(self, powerline, next_segment=None):
        if next_segment:
            separator_bg = powerline.bgcolor(next_segment.bg)
        else:
            separator_bg = powerline.reset

        return ''.join((
            powerline.fgcolor(self.fg),
            powerline.bgcolor(self.bg),
            self.content,
            separator_bg,
            powerline.fgcolor(self.separator_fg),
            self.separator))

def is_hg_clean():
    try:
        output = os.popen("hg status 2> /dev/null | grep -P '^[^?]' | tail -n1").read()
        return len(output) == 0
    except subprocess.CalledProcessError:
        return 0

def add_hg_segment(powerline, cwd):
    green = 148
    red = 161
    try:
        output = os.popen('hg branch 2> /dev/null').read()
        if len(output) > 0:
            branch = output.rstrip()
            bg = red
            fg = 15
            if is_hg_clean():
                bg = green
                fg = 0
            powerline.append(Segment(' %s ' % branch, fg, bg))
        else:
            return False
    except OSError:
        return False
    return True

def is_git_clean():
    # [[ $(git status 2> /dev/null | tail -n1) != "nothing to commit (working directory clean)" ]] && echo "*"
    try:
        output = os.popen('git status 2> /dev/null | tail -n1 | grep "nothing to commit (working directory clean)" ').read()
        return len(output) > 0
    except subprocess.CalledProcessError:
        return 0

def git_has_untracked_files():
    try:
        output = os.popen('git status 2> /dev/null | grep "Untracked files" ').read()
        return len(output) > 0
    except subprocess.CalledProcessError:
        return 0

def add_git_segment(powerline, cwd):
    if not os.path.exists(os.path.join(cwd,'.git')):
        return
    green = 148
    red = 161
    try:
        #cmd = "git branch 2> /dev/null | grep -e '\\*'"
        p1 = subprocess.Popen(['git', 'branch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(['grep', '-e', '\\*'], stdin=p1.stdout, stdout=subprocess.PIPE)
        output = p2.communicate()[0].strip()
        if len(output) == 0: return false
        branch = output.rstrip()[2:]
        if git_has_untracked_files():
            branch += ' +'
        bg = red
        fg = 15
        if is_git_clean():
            bg = green
            fg = 0
        powerline.append(Segment(' %s ' % branch, fg, bg))
    # if git or grep is not installed on the machine
    except OSError:
        return False
    except subprocess.CalledProcessError:
        return False
    return True

def add_svn_segment(powerline, cwd):
    if not os.path.exists(os.path.join(cwd,'.svn')):
        return
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
            powerline.append(Segment(' %s ' % changes, 22, 148))
    # if svn or grep is not installed on the machine
    except OSError:
        return False
    except subprocess.CalledProcessError:
        return False
    return True

# Show working directory with fancy separators
def add_cwd_segment(powerline, cwd, maxdepth):
    #powerline.append(' \\w ', 15, 237)
    home = os.getenv('HOME')
    cwd = os.getenv('PWD')

    if cwd.find(home) == 0:
        cwd = cwd.replace(home, '~', 1)

    if cwd[0] == '/':
        cwd = cwd[1:]

    names = cwd.split('/')
    if len(names) > maxdepth:
        names = names[:2] + ['⋯ '] + names[2-maxdepth:]

    for n in names[:-1]:
        powerline.append(Segment(' %s ' % n, 250, 237, Powerline.separator_thin, 244))
    powerline.append(Segment(' %s ' % names[-1], 254, 237))

def add_root_indicator(powerline, error):
    bg = 236
    fg = 15
    if int(error) != 0:
        fg = 15
        bg = 161
    powerline.append(Segment(' \\$ ', fg, bg))

if __name__ == '__main__':
    p = Powerline()
    cwd = os.getcwd()
    p.append(Segment(' \\u ', 250, 240))
    p.append(Segment(' \\h ', 250, 238))
    add_cwd_segment(p, cwd, 6)

    for add_repo_segment in [add_git_segment, add_svn_segment, add_hg_segment]:
        if add_repo_segment(p, cwd):
            break
    add_root_indicator(p, sys.argv[1] if len(sys.argv) > 1 else 0)
    sys.stdout.write(p.draw())
