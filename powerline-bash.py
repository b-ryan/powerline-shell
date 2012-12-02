#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import re

class Color:
    PATH_BG = 237
    PATH_FG = 250
    CWD_BG = 237
    CWD_FG = 254
    SEPARATOR_FG = 244

    REPO_CLEAN_BG = 148 # a light green color
    REPO_CLEAN_FG = 0 # black
    REPO_DIRTY_BG = 161 # pink/red
    REPO_DIRTY_FG = 15 # white

    CMD_PASSED_BG = 236
    CMD_PASSED_FG = 15
    CMD_FAILED_BG = 161
    CMD_FAILED_FG = 15

class Powerline:
    symbols = {
        'compatible': {
            'separator': u'\u25B6',
            'separator_thin': u'\u276F'
        },
        'patched': {
            'separator': u'\u2B80',
            'separator_thin': u'\u2B81'
        }
    }
    LSQESCRSQ = '\\[\\e%s\\]'
    reset = LSQESCRSQ % '[0m'

    def __init__(self, mode='compatible'):
        self.separator = Powerline.symbols[mode]['separator']
        self.separator_thin = Powerline.symbols[mode]['separator_thin']
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
        return (''.join((s[0].draw(s[1]) for s in zip(self.segments, self.segments[1:]+[None])))
            + self.reset).encode('utf-8')

class Segment:
    def __init__(self, powerline, content, fg, bg, separator=None, separator_fg=None):
        self.powerline = powerline
        self.content = content
        self.fg = fg
        self.bg = bg
        self.separator = separator or powerline.separator
        self.separator_fg = separator_fg or bg

    def draw(self, next_segment=None):
        if next_segment:
            separator_bg = self.powerline.bgcolor(next_segment.bg)
        else:
            separator_bg = self.powerline.reset

        return ''.join((
            self.powerline.fgcolor(self.fg),
            self.powerline.bgcolor(self.bg),
            self.content,
            separator_bg,
            self.powerline.fgcolor(self.separator_fg),
            self.separator))

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
        names = names[:2] + [u'\u2026'] + names[2-maxdepth:]

    for n in names[:-1]:
        powerline.append(Segment(powerline, ' %s ' % n, Color.PATH_FG, Color.PATH_BG, powerline.separator_thin, Color.SEPARATOR_FG))
    powerline.append(Segment(powerline, ' %s ' % names[-1], Color.CWD_FG, Color.CWD_BG))

def get_hg_status():
    has_modified_files = False
    has_untracked_files = False
    has_missing_files = False
    output = subprocess.Popen(['hg', 'status'], stdout=subprocess.PIPE).communicate()[0]
    for line in output.split('\n'):
        if line == '':
            continue
        elif line[0] == '?':
            has_untracked_files = True
        elif line[0] == '!':
            has_missing_files = True
        else:
            has_modified_files = True
    return has_modified_files, has_untracked_files, has_missing_files

def add_hg_segment(powerline, cwd):
    branch = os.popen('hg branch 2> /dev/null').read().rstrip()
    if len(branch) == 0:
        return False
    bg = Color.REPO_CLEAN_BG
    fg = 0
    has_modified_files, has_untracked_files, has_missing_files = get_hg_status()
    if has_modified_files or has_untracked_files or has_missing_files:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG
        extra = ''
        if has_untracked_files:
            extra += '+'
        if has_missing_files:
            extra += '!'
        branch += (' ' + extra if extra != '' else '')
    powerline.append(Segment(powerline, ' %s ' % branch, fg, bg))
    return True

def get_git_status():
    has_pending_commits = True
    has_untracked_files = False
    origin_position = ""
    output = subprocess.Popen(['git', 'status', '--ignore-submodules'], stdout=subprocess.PIPE).communicate()[0]
    for line in output.split('\n'):
        origin_status = re.findall("Your branch is (ahead|behind).*?(\d+) comm", line)
        if len(origin_status) > 0:
            origin_position = " %d" % int(origin_status[0][1])
            if origin_status[0][0] == 'behind':
                origin_position += u'\u21E3'
            if origin_status[0][0] == 'ahead':
                origin_position += u'\u21E1'

        if line.find('nothing to commit') >= 0:
            has_pending_commits = False
        if line.find('Untracked files') >= 0:
            has_untracked_files = True
    return has_pending_commits, has_untracked_files, origin_position

def add_git_segment(powerline, cwd):
    #cmd = "git branch 2> /dev/null | grep -e '\\*'"
    p1 = subprocess.Popen(['git', 'branch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', '-e', '\\*'], stdin=p1.stdout, stdout=subprocess.PIPE)
    output = p2.communicate()[0].strip()
    if len(output) == 0:
        return False
    branch = output.rstrip()[2:]
    has_pending_commits, has_untracked_files, origin_position = get_git_status()
    branch += origin_position
    if has_untracked_files:
        branch += ' +'
    bg = Color.REPO_CLEAN_BG
    fg = 0
    if has_pending_commits:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG
    powerline.append(Segment(powerline, ' %s ' % branch, fg, bg))
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
            powerline.append(Segment(powerline, ' %s ' % changes, 22, Color.REPO_CLEAN_BG))
    except OSError:
        return False
    except subprocess.CalledProcessError:
        return False
    return True

def add_repo_segment(powerline, cwd):
    for add_repo_segment in [add_git_segment, add_svn_segment, add_hg_segment]:
        try:
            if add_repo_segment(p, cwd): return
        except subprocess.CalledProcessError:
            pass
        except OSError:
            pass

def add_virtual_env_segment(powerline, cwd):
    env = os.getenv("VIRTUAL_ENV")
    if env == None:
        return False
    env_name = os.path.basename(env)
    bg = 35
    fg = 22
    powerline.append(Segment(powerline,' %s ' % env_name, fg, bg))
    return True


def add_root_indicator(powerline, error):
    bg = Color.CMD_PASSED_BG
    fg = Color.CMD_PASSED_FG
    if int(error) != 0:
        fg = Color.CMD_FAILED_FG
        bg = Color.CMD_FAILED_BG
    powerline.append(Segment(powerline, ' \\$ ', fg, bg))

if __name__ == '__main__':
    p = Powerline(mode='patched')
    cwd = os.getcwd()
    add_virtual_env_segment(p, cwd)
    #p.append(Segment(powerline, ' \\u ', 250, 240))
    #p.append(Segment(powerline, ' \\h ', 250, 238))
    add_cwd_segment(p, cwd, 5)
    add_repo_segment(p, cwd)
    add_root_indicator(p, sys.argv[1] if len(sys.argv) > 1 else 0)
    sys.stdout.write(p.draw())

# vim: set expandtab:
