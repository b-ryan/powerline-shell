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
            'separator': u'\u25B6',
            'separator_thin': u'\u276F',
            'lseparator': u'\u25c2',
            'lseparator_thin': u'\u276e'
        },
        'patched': {
            'separator': u'\u2B80',
            'separator_thin': u'\u2B81',
            'lseparator': u'\u2B82',
            'lseparator_thin': u'\u2B83'
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
        return (''.join((s[0].draw(self, s[1]) for s in zip(self.segments, self.segments[1:]+[None])))
            + self.reset).encode('utf-8')


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

        return ''.join((
            powerline.fgcolor(self.fg),
            powerline.bgcolor(self.bg),
            self.content,
            separator_bg,
            powerline.fgcolor(self.separator_fg),
            get_separator(self.separator)))


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


def add_hg_segment(cwd):
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
    output = subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE).communicate()[0]
    for line in output.split('\n'):
        origin_status = re.findall("Your branch is (ahead|behind).*?(\d+) comm", line)
        if len(origin_status) > 0:
            origin_position = " %d" % int(origin_status[0][1])
            if origin_status[0][0] == 'behind':
                origin_position += u'\u21E3'
            if origin_status[0][0] == 'ahead':
                origin_position += u'\u21E1'

        if line.find('nothing to commit (working directory clean)') >= 0:
            has_pending_commits = False
            has_not_staged = False
        if line.find('Changes not staged for commit:') >= 0:
            has_not_staged = True
        if line.find('Changes to be committed:') >= 0:
            has_pending_commits = True
        if line.find('Untracked files') >= 0:
            has_untracked_files = True
    return has_not_staged, has_pending_commits, has_untracked_files, origin_position

def add_git_segment(cwd):
    bg = 148
    fg = 8
    p1 = subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p1.communicate()[0].strip()
    if len(output) == 0:
        fg=34
        bg=22
        return Segment(' git ', fg, bg)
    else:
        branch = output.splitlines()[0].rstrip()[12:]
        has_not_staged, has_pending_commits, has_untracked_files, origin_position = get_git_status()

    segments = [
            Segment(' git ' , fg, bg, 'thin', fg),
            Segment(' w:%s ' % ('+' if has_not_staged else u'✔') , fg, bg, 'thin',fg),
            Segment(' i:%s ' % ('+' if has_pending_commits else u'✔'), fg, bg, 'thin',fg),
            Segment(' r:%s ' % branch, fg, bg),
    ]
    return segments

def add_svn_segment(cwd):
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

def add_repo_segment(cwd):
    for add_repo_segment in [add_git_segment, add_svn_segment, add_hg_segment]:
        try:
            info = add_repo_segment(cwd)
            if info:
                return info
        except subprocess.CalledProcessError:
            pass
        except OSError:
            pass

def add_virtual_env_segment(cwd):
    env = os.getenv("VIRTUAL_ENV")
    if env == None:
        env_name = '-'
        bg = 23
        fg = 35
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


def developer_powerline():
    p = Powerline(mode='patched')
    cwd = os.getcwd()
    p.append(Segment(" - dev mode -",7,1))
    p.append(add_virtual_env_segment(cwd))
    p.append(add_repo_segment(cwd))
    p.append(NewLineSegment())
    sys.stdout.write(p.draw())

def add_time():
    from datetime import datetime
    return Segment(datetime.now().strftime(' %H:%M:%S '),228,34)

def add_timer(min_time=5):
    #TODO: eh, bash and its signals ;]
    return
    last = os.getenv('LAST_CMD_TIME', None)
    fg = 99
    bg = 89
    if not last:
        return
    else:
        segments = [Segment(' Last cmd ',bg,fg, )]
        from datetime import datetime, timedelta
        try:
            start = int(os.getenv('LAST_CMD_TIME'))
            start = datetime.fromtimestamp(start)
        except Exception as error:
            return segments + [Segment(' Error while parsing date from LAST_CMD_TIME: %s '%error, fg, bg)]
        now = int(os.getenv('LAST_CMD_TIME'))
        now = datetime.fromtimestamp(now)
        if now - start < timedelta(seconds=min_time):
            return
        segments.extend((
                Segment(' start:%s '%start,fg, bg,'thin', fg),
                Segment(' stop:%s '%now,fg, bg, 'thin', fg),
                Segment(' time:%s '%(now-start,),fg, bg)
                ))
        return segments


if __name__ == '__main__':
    print 

    timer = add_timer()
    if timer:
        p = Powerline(mode='patched')
        p.append(timer)
        p.append(NewLineSegment())
        sys.stdout.write(p.draw())

    cwd = os.getcwd()
    if os.getenv('POWERLINE_DEVELMODE',None):
        developer_powerline()
    p = Powerline(mode='patched')
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
