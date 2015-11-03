import subprocess


def add_git_stash_segment():
    stash_count = subprocess.check_output('git stash list | wc -l', shell=True).strip()

    if stash_count == '0':
        return

    bg = Color.REPO_DIRTY_BG
    fg = Color.REPO_DIRTY_FG

    powerline.append('(%s)' % (stash_count,), fg, bg)

try:
    add_git_stash_segment()
except OSError:
    pass
except subprocess.CalledProcessError:
    pass
