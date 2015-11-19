import os
import subprocess

HG_SYMBOLS = {
    'added': u'\u2713',
    'modified': u'\u270E',
    'removed': u'\u2715',
    'missing': u'\u0021',
    'untracked': u'?'
}

def _is_repo_dirty(stats):
    dirty = False
    for key, value in stats.iteritems():
        if value > 0:
            dirty = True
    return dirty

def _n_or_empty(_dict, _key):
    return _dict[_key] if int(_dict[_key]) > 1 else u''

def get_hg_status():
    stats = {'added': 0, 'modified': 0, 'removed': 0, 'missing': 0, 'untracked': 0}
    output = subprocess.Popen(['hg', 'status'],
            stdout=subprocess.PIPE).communicate()[0]
    for line in output.split('\n'):
        if line == '':
            continue
        elif line[0] == 'A':
            stats['added'] += 1
        elif line[0] == 'M':
            stats['modified'] += 1
        elif line[0] == 'R':
            stats['removed'] += 1
        elif line[0] == '!':
            stats['missing'] += 1
        elif line[0] == '?':
            stats['untracked'] += 1
    return stats

def add_hg_segment():
    branch = os.popen('hg branch 2> /dev/null').read().rstrip()
    if len(branch) == 0:
        return False
    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG

    stats = get_hg_status()

    if _is_repo_dirty(stats):
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG

        powerline.append(' %s ' % branch, fg, bg)

        def _add(_dict, _key, fg, bg):
            if _dict[_key]:
                _str = u' {}{} '.format(_n_or_empty(_dict, _key), HG_SYMBOLS[_key])
                powerline.append(_str, fg, bg)

        _add(stats, 'added', Color.HG_ADDED_FG, Color.HG_ADDED_BG)
        _add(stats, 'modified', Color.HG_MODIFIED_FG, Color.HG_MODIFIED_BG)
        _add(stats, 'removed', Color.HG_REMOVED_FG, Color.HG_REMOVED_BG)
        _add(stats, 'missing', Color.HG_MISSING_FG, Color.HG_MISSING_BG)
        _add(stats, 'untracked', Color.HG_UNTRACKED_FG, Color.HG_UNTRACKED_BG)
    else:
        powerline.append(' %s ' % branch, fg, bg)


add_hg_segment()
