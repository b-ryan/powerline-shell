#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import re

class Palette:
    black=30
    red=31
    blue=32
    yellow=33
    green=34
    purple=35
    cyan=36
    white=37

class Powerline:
    symbols = {
        'compatible': {
            'separator': u'\u25B6'.encode('UTF-8'),
            'separator_thin': u'\u276F'.encode('UTF-8'),
            'lseparator': u'\u25c2'.encode('UTF-8'),
            'lseparator_thin': u'\u276e'.encode('UTF-8')
        },
        'patched': {
            'separator': u'\u2B80'.encode('UTF-8'),
            'separator_thin': u'\u2B81'.encode('UTF-8'),
            'lseparator': u'\u2B82'.encode('UTF-8'),
            'lseparator_thin': u'\u2B83'.encode('UTF-8')
        }
    }
    LSQESCRSQ = '\\[\\e%s\\]'
    reset = LSQESCRSQ % '[0m'

    def __init__(self, mode='compatible', direction='right', palette=Palette):
        if direction == 'right':
            self.separator = Powerline.symbols[mode]['separator']
            self.separator_thin = Powerline.symbols[mode]['separator_thin']
        elif direction == 'left':
            self.separator = Powerline.symbols[mode]['lseparator']
            self.separator_thin = Powerline.symbols[mode]['lseparator_thin']
        else:
            raise Exception('direction can be "left" or "right"')
        self.segments = []
        self.palette = palette

    def translate_color(self, color):
        if isinstance(color, int):
            return color
        elif isinstance(color, basestring):
            try:
                return getattr(self.palette, color)
            except AttributeError:
                raise Exception("There is no '%s' color defined in palette."%color)
        else:
            raise Exception("You can pick colors using ints or names defined in palette.")

    def color(self, prefix, code):
        return self.LSQESCRSQ % ('[%s;5;%sm' % (prefix, code))

    def fgcolor(self, code):
        return self.color('38', self.translate_color(code))

    def bgcolor(self, code):
        return self.color('48', self.translate_color(code))

    def append(self, segment):
        '''
        Add segment to Powerline

        :param segment: can be `Segment` instance or list/tuple of Segments If
            None, True, False is passed, nothing will be rendered (backward
            compatibility)
        '''

        if isinstance(segment, Segment):
            self.segments.append(segment)
        elif isinstance(segment, (list, tuple)):
            for segment_ in segment:
                self.append(segment_)
        elif segment in (None, False, True):
            pass
        else:
            Exception("%s - this segment type is not allowed. Use Segment instance."%type(segment))

    def draw(self):
        content = (''.join((s[0].draw(self, s[1]) for s in zip(self.segments, self.segments[1:]+[None])))
            + self.reset)
        return content


class Segment(object):
    def __init__(self, content, fg, bg, separator=None, separator_fg=None):
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

        def get_separator(sep):
            if sep=='thin':
                return powerline.separator_thin
            elif sep in ('full', None):
                return powerline.separator
            else:
                return sep

        x=str(''.join((
            powerline.fgcolor(self.fg),
            powerline.bgcolor(self.bg),
            self.content,
            separator_bg,
            powerline.fgcolor(self.separator_fg),
            get_separator(self.separator))))
        return x


class NewLineSegment(Segment):
    def __init__(self):
        #super(NewLineSegment, self).__init__(None, '',0,0)
        self.fg=1
        self.bg=00
        pass


    def draw(self, powerline,  next_segment=None):
        return ''.join((powerline.reset, '\\n'))


def add_cwd_segment(cwd, maxdepth):
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

    segments = []
    segments.append(Segment(' ' , 39, 24))
    for n in names[:-1]:
        segments.append(Segment('%s' % n, 39, 24, '/', 190))
    segments.append(Segment('%s ' % names[-1], 7, 24))
    return segments


def is_hg_clean():
    output = os.popen("hg status 2> /dev/null | grep '^?' | tail -n1").read()
    return len(output) == 0


def add_hg_segment(cwd, return_none):
    green = 148
    red = 161
    branch = os.popen('hg branch 2> /dev/null').read().rstrip()
    if len(branch) == 0:
        return False
    bg = red
    fg = 15
    if is_hg_clean():
        bg = green
        fg = 0
    return Segment(' %s ' % branch, fg, bg)

def get_git_status():
    has_pending_commits = False
    has_not_staged = False
    has_untracked_files = False
    origin_position = ""
    branch = ""
    output = subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE).communicate()[0]
    output = output.splitlines()
    if len(output) == 0:
        is_git = False
        return False, None, None, None, None, None
    else:
        is_git = True

    if re.findall('Not currently on any', output[0]):
        branch = 'NO BRANCH'
    elif re.findall('On branch', output[0]):
        branch = output[0][12:]
    else:
        branch = 'ERROR'

    for line in output:
        origin_status = re.findall("Your branch is (ahead|behind) .* (\d+) commit", line)
        if len(origin_status) > 0:
            origin_position = "%d" % int(origin_status[0][1])
            if origin_status[0][0] == 'behind':
                origin_position += u'\u21E3'.encode('UTF-8')
            elif origin_status[0][0] == 'ahead':
                origin_position += u'\u21E1'.encode('UTF-8')
            else:
                origin_position = ''

        if line.find('nothing to commit (working directory clean)') >= 0:
            has_pending_commits = False
            has_not_staged = False
        if line.find('Changes not staged for commit:') >= 0:
            has_not_staged = True
        if line.find('Changes to be committed:') >= 0:
            has_pending_commits = True
        if line.find('Untracked files') >= 0:
            has_untracked_files = True
    return is_git, branch, has_not_staged, has_pending_commits, has_untracked_files, origin_position


def add_git_segment(cwd, return_none):
    ok = u'✔'.encode('UTF-8')
    dirty = '+'
    bg = 148
    fg = 8

    is_git, branch, has_not_staged, has_pending_commits, has_untracked_files, origin_position = get_git_status()

    if not is_git:
        if return_none:
            return None
        else:
            return Segment(' git ', fg, bg)

    if origin_position:
        branch = '%s(%s)' % (branch, origin_position)

    segments = [
            Segment(' git ' , fg, bg, 'thin', fg),
            Segment(' w:%s ' % (dirty if has_not_staged else ok) , fg, bg, 'thin',fg),
            Segment(' i:%s ' % (dirty if has_pending_commits else ok), fg, bg, 'thin',fg),
            Segment(' r:%s ' % branch, fg, bg),
    ]
    return segments


def add_svn_segment(cwd, return_none):
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
            return Segment(' %s ' % changes, 22, 148)
    except OSError:
        return False
    except subprocess.CalledProcessError:
        return False
    return True


def add_repo_segment(cwd, return_none=True):
    for _add_repo_segment in [add_git_segment, add_svn_segment, add_hg_segment]:
        try:
            info = _add_repo_segment(cwd, return_none)
            if info:
                return info
        except subprocess.CalledProcessError:
            pass
        except OSError:
            pass


def add_virtual_env_segment(cwd, return_none=True):
    env = os.getenv("VIRTUAL_ENV")
    if env is None:
        env_name = '-'
        bg = 23
        fg = 35
        if return_none:
            return
    else:
        env_name = os.path.basename(env)
        bg = 35
        fg = 51
    return Segment(' VE ', fg, bg, 'thin', fg),  Segment(' %s ' % env_name, fg, bg)


def add_error_code(error):
    bg = 236
    fg = 15
    if int(error) != 0:
        fg = 15
        bg = 161
        return Segment(' %s '%error, fg, bg)
    return Segment(' %s '%error, fg, bg, 'thin',fg)

def add_root_indicator():
    bg = 236
    fg = 15
    #TODO
    return Segment(r' \$', fg, bg,)


def set_terminal_title_to_pwd():
    sys.stdout.write('\033]0;(${PWD}) - terminal\007')


def developer_powerline():
    dev_mode = os.getenv('POWERLINE_DEVELMODE', '')

    if not dev_mode:
        return

    p = Powerline(mode='patched')
    cwd = os.getcwd()
    p.append(Segment(" - dev mode -",7,1))

    segments = (add_virtual_env_segment(cwd),
                add_repo_segment(cwd))

    if dev_mode.lower() in ('?', 'auto') and not filter(bool, segments):
        return

    for segment in segments:
        p.append(segment)
    p.append(NewLineSegment())
    sys.stdout.write(p.draw())


def add_time():
    from datetime import datetime
    return Segment(datetime.now().strftime(' %H:%M:%S '),228,34)


if __name__ == '__main__':
    print

    cwd = os.getcwd()
    developer_powerline()

    p = Powerline(mode='patched')
    p.append(set_terminal_title_to_pwd())
    p.append(add_time())
    p.append(Segment(' \\u', 9, 185, ''))
    p.append(Segment('@', 17, 185, ''))
    p.append(Segment('\\h', 9, 185))
    p.append(add_cwd_segment(cwd, 5))
    p.append(NewLineSegment())
    sys.stdout.write(p.draw())

    p = Powerline(mode='patched')
    p.append(add_error_code(sys.argv[1] if len(sys.argv) > 1 else 0))
    p.append(add_root_indicator())
    sys.stdout.write(p.draw())

# vim: set expandtab:
