import re
import subprocess

def get_git_status(pdata):
    status = pdata[0].splitlines()

    branchinfo = re.search('^## (?P<local>\S+?)(\.{3}(?P<remote>\S+?)( \[(ahead (?P<ahead>\d+)(, )?)?(behind (?P<behind>\d+))?\])?)?$', status[0])

    stats = {'untracked': 0, 'notstaged': 0, 'staged': 0, 'conflicted': 0}
    for statusline in status[1:]:
        code = statusline[:2]
        if code == '??':
            stats['untracked'] += 1
        elif code in ('DD', 'AU', 'UD', 'UA', 'DU', 'AA', 'UU'):
            stats['conflicted'] += 1
        else:
            if code[1] != ' ':
                stats['notstaged'] += 1
            if code[0] != ' ':
                stats['staged'] += 1
    dirty = (True if sum(stats.values()) > 0 else False)
    return dirty, stats, branchinfo.groupdict() if branchinfo else None


def add_git_segment():
    symbols = {
        'detached': u'\u2693',
        'ahead': u'\u2B06',
        'behind': u'\u2B07',
        'staged': u'\u2714',
        'notstaged': u'\u270E',
        'conflicted': u'\u273C'
    }

    p = subprocess.Popen(['git', 'status', '--porcelain', '-b'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pdata = p.communicate()
    if p.returncode != 0:
        return

    dirty, stats, branchinfo = get_git_status(pdata)

    if branchinfo:
        branch = branchinfo['local']
    else:
        p = subprocess.Popen(['git', 'describe', '--tags', '--always'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        detached_ref = p.communicate()[0].rstrip('\n')
        if p.returncode == 0:
            branch = '%c %s' % (symbols['detached'], detached_ref.decode('utf-8'))
        else:
            branch = 'Big Bang'

    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
    if dirty:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG

    powerline.append(' %s ' % branch, fg, bg)

    if branchinfo:
        if branchinfo['ahead']:
            powerline.append('%s%c' % (branchinfo['ahead'] if int(branchinfo['ahead']) > 1 else str('').decode('utf-8'), symbols['ahead']), Color.GIT_AHEAD_FG, Color.GIT_AHEAD_BG)
        if branchinfo['behind']:
            powerline.append('%s%c' % (branchinfo['behind'] if int(branchinfo['behind']) > 1 else str('').decode('utf-8'), symbols['behind']), Color.GIT_BEHIND_FG, Color.GIT_BEHIND_BG)
    if stats['staged']:
        powerline.append('%s%c' % (stats['staged'] if stats['staged'] > 1 else str('').decode('utf-8'), symbols['staged']), Color.GIT_STAGED_FG, Color.GIT_STAGED_BG)
    if stats['notstaged']:
        powerline.append('%s%c' % (stats['notstaged'] if stats['notstaged'] > 1 else str('').decode('utf-8'), symbols['notstaged']), Color.GIT_NOTSTAGED_FG, Color.GIT_NOTSTAGED_BG)
    if stats['untracked']:
        powerline.append('%s?' % (stats['untracked'] if stats['untracked'] > 1 else str('')), Color.GIT_UNTRACKED_FG, Color.GIT_UNTRACKED_BG)
    if stats['conflicted']:
        powerline.append('%s%c' % (stats['conflicted'] if stats['conflicted'] > 1 else str('').decode('utf-8'), symbols['conflicted']), Color.GIT_CONFLICTED_FG, Color.GIT_CONFLICTED_BG)
try:
    add_git_segment()
except OSError:
    pass
except subprocess.CalledProcessError:
    pass
