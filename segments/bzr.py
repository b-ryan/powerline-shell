from bzrlib import bzrdir, urlutils, workingtree, status, errors
from StringIO import StringIO
import os

COLOCATED_LOCATION = '.bzr/branches'

def add_bzr_segment():
    location = os.getcwd()

    try:
        a_bzrdir, extra_path = bzrdir.BzrDir.open_containing(location)
    except errors.NotBranchError:
        return False

    branch = a_bzrdir.open_branch()
    try:
        # colocated branch
        base = branch.base[:branch.base.index(COLOCATED_LOCATION)]
        repo_location = urlutils.join(base, COLOCATED_LOCATION)
        name = branch.base[len(repo_location):].strip('/')
    except ValueError:
        # classic branch
        base = branch.base
        repo_location = base
        name = branch.nick

    working = workingtree.WorkingTree.open(base)

    has_modified_files, has_untracked_files, has_missing_files = False, False, False

    tof = StringIO()
    status.show_tree_status(working, short=True, to_file=tof)
    tof.seek(0)
    values = tof.readlines()

    for line in values:
        if line.split()[0] == 'M':
            has_modified_files
        elif line.split()[0] == '?':
            has_untracked_files = True
        elif line.split()[0] == 'D':
            has_missing_files = True

    if has_modified_files or has_untracked_files or has_missing_files:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG
    else:
        bg = Color.REPO_CLEAN_BG
        fg = Color.REPO_CLEAN_FG

    name = has_missing_files and name+'!' or has_untracked_files and name+'+' or name
    return powerline.append(' %s ' % name, fg, bg)

add_bzr_segment()
