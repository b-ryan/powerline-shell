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

    try:
        working = workingtree.WorkingTree.open(base)
    except errors.MissingFeature:
        working = False
    has_modified_files, has_untracked_files, has_missing_files = False, False, False

    if working:
        tof = StringIO()
        status.show_tree_status(working, short=True, to_file=tof)
        tof.seek(0)
        statuses = set(l.strip()[0] for l in tof.readlines())
        for s in statuses:
            if s == 'M':
                has_modified_files = True
            elif s == '?':
                has_untracked_files = True
            elif s == 'D':
                has_missing_files = True

    if has_modified_files or has_missing_files:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG
    else:
        bg = Color.REPO_CLEAN_BG
        fg = Color.REPO_CLEAN_FG

    name = has_missing_files and name+'!' or has_untracked_files and name+'+' or name
    return powerline.append(' %s ' % name, fg, bg)

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import os

try:
    from bzrlib import bzrdir, urlutils, workingtree, status, errors
    add_bzr_segment()
except ImportError:
    pass
