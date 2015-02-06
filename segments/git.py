"""
Add the Git segment to the Powerline-shell prompt
"""
import os
import re
import subprocess


def get_git_status():
    """
    Get the status of the Git repository
    """
    has_pending_commits = True
    has_untracked_files = False
    origin_position = ""
    output = subprocess.Popen(['git', 'status', '--ignore-submodules'],
                              env={"LANG": "C", "HOME": os.getenv("HOME")},
                              stdout=subprocess.PIPE).communicate()[0]
    try:
        lines = output.split('\n')
    except TypeError:  # Python 3
        lines = output.decode().split('\n')
    for line in lines:
        origin_status = re.findall(
            r"Your branch is (ahead|behind).*?(\d+) comm", line)
        diverged_status = re.findall(r"and have (\d+) and (\d+) different commits each", line)
        if origin_status:
            origin_position = " %d" % int(origin_status[0][1])
            if origin_status[0][0] == 'behind':
                origin_position += u'\u21E3'
            if origin_status[0][0] == 'ahead':
                origin_position += u'\u21E1'
        if diverged_status:
            origin_position = " %d%c %d%c" % (int(diverged_status[0][0]), u'\u21E1', int(diverged_status[0][1]), u'\u21E3')

        if line.find('nothing to commit') >= 0:
            has_pending_commits = False
        if line.find('Untracked files') >= 0:
            has_untracked_files = True
    return has_pending_commits, has_untracked_files, origin_position


def add_git_segment():
    """
    Add the Git segment to the Powerline-shell prompt

    This version of the function fails quickly
    """
    oldcwd = os.getcwd()
    # Fail quickly if .git is not present in cwd and parents
    found = False
    pathhead, pathtail = oldcwd, '.'
    while pathtail != '':
        if os.access(".git", os.R_OK):
            found = True
            break
        pathhead, pathtail = os.path.split(pathhead)

    # If we aren't anywhere inside a Git repository, bail
    if not found:
        return

    try:
        os.chdir(pathhead)
        # See http://git-blame.blogspot.com/2013/06/checking-current-branch-programatically.html
        p = subprocess.Popen(['git', 'symbolic-ref', '-q', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

    if 'Not a git repo' in str(err):
        return

        if out:
            branch = out[len('refs/heads/'):].rstrip()
        else:
            branch = '(Detached)'

    has_pending_commits, has_untracked_files, origin_position = get_git_status()
    try:
        branch += origin_position
    except TypeError:
        branch = branch.decode()
        branch += origin_position
    if has_untracked_files:
        branch += ' +'

        bg = Color.REPO_CLEAN_BG
        fg = Color.REPO_CLEAN_FG
        if has_pending_commits:
            bg = Color.REPO_DIRTY_BG
            fg = Color.REPO_DIRTY_FG

        powerline.append(' %s ' % branch, fg, bg)

    except OSError:
        pass
    except subprocess.CalledProcessError:
        pass
    finally:  # Execute unconditionally, regardless of what happened in the try/except blocks
        os.chdir(oldcwd)
