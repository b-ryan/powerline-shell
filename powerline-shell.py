#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import re
import argparse

def warn(msg):
    print '[powerline-bash] ', msg


class Color:
    # The following link is a pretty good resources for color values:
    # http://www.calmar.ws/vim/color-output.png

    PATH_BG = 237  # dark grey
    PATH_FG = 250  # light grey
    CWD_FG = 254  # nearly-white grey
    SEPARATOR_FG = 244

    REPO_CLEAN_BG = 148  # a light green color
    REPO_CLEAN_FG = 0  # black
    REPO_DIRTY_BG = 161  # pink/red
    REPO_DIRTY_FG = 15  # white

    CMD_PASSED_BG = 236
    CMD_PASSED_FG = 15
    CMD_FAILED_BG = 161
    CMD_FAILED_FG = 15

    SVN_CHANGES_BG = 148
    SVN_CHANGES_FG = 22  # dark green

    VIRTUAL_ENV_BG = 35  # a mid-tone green
    VIRTUAL_ENV_FG = 00


class Powerline:
    symbols = {
        'compatible': {
            'separator': u'\u25B6',
            'separator_thin': u'\u276F'
        },
        'patched': {
            'separator': u'\u2B80',
            'separator_thin': u'\u2B81'
        },
        'flat': {
            'separator': '',
            'separator_thin': ''
        },
    }

    color_templates = {
        'bash': '\\[\\e%s\\]',
        'zsh': '%%{%s%%}',
        'bare': '%s',
    }

    root_indicators = {
        'bash': ' \\$ ',
        'zsh': ' \\$ ',
        'bare': ' $ ',
    }

    user_prompt = {
        'bash': ' \\u',
        'zsh': ' %n'
    }

    host_prompt = {
        'bash': ' \\h',
        'zsh': ' %m'
    }

    def __init__(self, mode, shell):
        self.shell = shell
        self.color_template = self.color_templates[shell]
        self.root_indicator = self.root_indicators[shell]
        self.reset = self.color_template % '[0m'
        self.separator = Powerline.symbols[mode]['separator']
        self.separator_thin = Powerline.symbols[mode]['separator_thin']
        self.segments = []

    def color(self, prefix, code):
        return self.color_template % ('[%s;5;%sm' % (prefix, code))

    def fgcolor(self, code):
        return self.color('38', code)

    def bgcolor(self, code):
        return self.color('48', code)

    def append(self, segment):
        self.segments.append(segment)

    def draw(self):
        shifted = self.segments[1:] + [None]
        return (''.join((c.draw(n) for c, n in zip(self.segments, shifted)))
                + self.reset).encode('utf-8')


class Segment:
    def __init__(self, powerline, content, fg, bg, separator=None,
            separator_fg=None):
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

def add_hostname_segment(powerline):
    hostname = socket.gethostname()
    user = os.getenv("USER")
    powerline.append(Segment(powerline, ' %s@%s ' % (user, hostname), Color.CWD_FG, Color.PATH_BG))


def add_cwd_segment(powerline, cwd, args):
    home = os.getenv('HOME')
    cwd = cwd or os.getenv('PWD')
    cwd = cwd.decode('utf-8')

    if cwd.find(home) == 0:
        cwd = cwd.replace(home, '~', 1)

    if cwd[0] == '/':
        cwd = cwd[1:]

    names = cwd.split(os.sep)
    if len(names) > args.cwd_max_depth:
        names = names[:2] + [u'\u2026'] + names[2 - args.cwd_max_depth:]

    if not args.cwd_only:
        for n in names[:-1]:
            powerline.append(Segment(powerline, ' %s ' % n, Color.PATH_FG,
                Color.PATH_BG, powerline.separator_thin, Color.SEPARATOR_FG))
    powerline.append(Segment(powerline, ' %s ' % names[-1], Color.CWD_FG,
        Color.PATH_BG))

def add_username_segment(p, cwd, args):
    p.append(Segment(p, p.user_prompt[p.shell], 250, 240))

def add_hostname_segment(p, cwd, args):
    p.append(Segment(p, p.host_prompt[p.shell], 250, 238))

def get_hg_status():
    has_modified_files = False
    has_untracked_files = False
    has_missing_files = False
    output = subprocess.Popen(['hg', 'status'],
            stdout=subprocess.PIPE).communicate()[0]
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

def get_fossil_status():
    has_modified_files = False
    has_untracked_files = False
    has_missing_files = False
    output = os.popen('fossil changes 2>/dev/null').read().strip()
    has_untracked_files = True if os.popen("fossil extras 2>/dev/null").read().strip() else False
    has_missing_files = 'MISSING' in output
    has_modified_files = 'EDITED' in output

    return has_modified_files, has_untracked_files, has_missing_files


def add_hg_segment(powerline, cwd, args):
    branch = os.popen('hg branch 2> /dev/null').read().rstrip()
    if len(branch) == 0:
        return False
    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
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

def add_fossil_segment(powerline, cwd, args):
    subprocess.Popen(['fossil'], stdout=subprocess.PIPE).communicate()[0]
    branch = ''.join([i.replace('*','').strip() for i in os.popen("fossil branch 2> /dev/null").read().strip().split("\n") if i.startswith('*')])
    if len(branch) == 0:
        return False

    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
    has_modified_files, has_untracked_files, has_missing_files = get_fossil_status()
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
    output = subprocess.Popen(['git', 'status', '--ignore-submodules'],
            stdout=subprocess.PIPE, env={'LC_MESSAGES':'C'}).communicate()[0]
    for line in output.split('\n'):
        origin_status = re.findall(
                r"Your branch is (ahead|behind).*?(\d+) comm", line)
        if origin_status:
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


def add_git_segment(powerline, cwd, args):
    #cmd = "git branch 2> /dev/null | grep -e '\\*'"
    p1 = subprocess.Popen(['git', 'branch', '--no-color'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', '-e', '\\*'], stdin=p1.stdout, stdout=subprocess.PIPE)
    output = p2.communicate()[0].strip()
    if not output:
        return False

    branch = output.rstrip()[2:]
    has_pending_commits, has_untracked_files, origin_position = get_git_status()
    branch += origin_position
    if has_untracked_files:
        branch += ' +'

    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
    if has_pending_commits:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG

    powerline.append(Segment(powerline, ' %s ' % branch, fg, bg))
    return True


def add_svn_segment(powerline, cwd, args):
    is_svn = subprocess.Popen(['svn', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    is_svn_output = is_svn.communicate()[1].strip()
    if len(is_svn_output) != 0:
        return

    try:
        #"svn status | grep -c "^[ACDIMRX\\!\\~]"
        p1 = subprocess.Popen(['svn', 'status'], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        p2 = subprocess.Popen(['grep', '-c', '^[ACDIMR\\!\\~]'],
                stdin=p1.stdout, stdout=subprocess.PIPE)
        output = p2.communicate()[0].strip()
        if len(output) > 0 and int(output) > 0:
            changes = output.strip()
            powerline.append(Segment(powerline, ' %s ' % changes,
                Color.SVN_CHANGES_FG, Color.SVN_CHANGES_BG))
    except OSError:
        return False
    except subprocess.CalledProcessError:
        return False
    return True


def add_virtual_env_segment(powerline, cwd, args):
    env = os.getenv("VIRTUAL_ENV")
    if env is None:
        return False

    env_name = os.path.basename(env)
    bg = Color.VIRTUAL_ENV_BG
    fg = Color.VIRTUAL_ENV_FG
    powerline.append(Segment(powerline, ' %s ' % env_name, fg, bg))
    return True


def add_root_indicator(powerline, cwd, args):
    bg = Color.CMD_PASSED_BG
    fg = Color.CMD_PASSED_FG
    if int(args.prev_error) != 0:
        fg = Color.CMD_FAILED_FG
        bg = Color.CMD_FAILED_BG
    powerline.append(Segment(powerline, powerline.root_indicator, fg, bg))


def get_valid_cwd():
    """ We check if the current working directory is valid or not. Typically
        happens when you checkout a different branch on git that doesn't have
        this directory.
        We return the original cwd because the shell still considers that to be
        the working directory, so returning our guess will confuse people
    """
    try:
        cwd = os.getcwd()
    except:
        cwd = os.getenv('PWD')  # This is where the OS thinks we are
        parts = cwd.split(os.sep)
        up = cwd
        while parts and not os.path.exists(up):
            parts.pop()
            up = os.sep.join(parts)
        try:
            os.chdir(up)
        except:
            warn("Your current directory is invalid.")
            sys.exit(1)
        warn("Your current directory is invalid. Lowest valid directory: " + up)
    return cwd

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--cwd-only', action='store_true',
            help='Only show the current directory')
    arg_parser.add_argument('--cwd-max-depth', action='store', type=int,
            default=5, help='Maximum number of directories to show in path')
    arg_parser.add_argument('--mode', action='store', default='patched',
            help='The characters used to make separators between segments',
            choices=['patched', 'compatible', 'flat'])
    arg_parser.add_argument('--shell', action='store', default='bash',
            help='Set this to your shell type', choices=['bash', 'zsh'])
    arg_parser.add_argument('prev_error', nargs='?', default=0,
            help='Error code returned by the last command')
    args = arg_parser.parse_args()

    p = Powerline(mode=args.mode, shell=args.shell)
    cwd = get_valid_cwd()

    # Comment or uncomment segments that you do not want:
    PROMPT_SEGMENTS = (
        add_virtual_env_segment,
        add_username_segment,
        add_hostname_segment,
        add_cwd_segment,
        add_git_segment,
        add_svn_segment,
        add_hg_segment,
        add_fossil_segment,
        add_root_indicator,
    )

    try:
        for add_segment in PROMPT_SEGMENTS:
            add_segment(p, cwd, args)
    except subprocess.CalledProcessError:
        pass
    except OSError:
        pass
    sys.stdout.write(p.draw())

# vim: set expandtab:
