import subprocess

def add_svn_segment():
    is_svn = subprocess.Popen(['svn', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    is_svn_output = is_svn.communicate()[1].strip()
    if len(is_svn_output) != 0:
        return

    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG

    # Current branch
    # LANG=C svn info | grep "^URL:" | grep -Eo "(tags|branches)/[^/]+|trunk" | grep -Eo "[^/]+$"
    bp1 = subprocess.Popen(['svn', 'info'], env={"LANG": "C"}, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    bp2 = subprocess.Popen(['grep', '^URL:'], stdin=bp1.stdout, stdout=subprocess.PIPE)
    bp3 = subprocess.Popen(['grep', '-Eo', '(tags|branches)/[^/]+|trunk'], stdin=bp2.stdout, stdout=subprocess.PIPE)
    bp4 = subprocess.Popen(['grep', '-Eo', '[^/]+$'], stdin=bp3.stdout, stdout=subprocess.PIPE)
    boutput = bp4.communicate()[0].strip()
    if len(boutput) > 0:
        changes = boutput
    else:
        changes = '(Unversioned)'

    # Number of changes
    # LANG=C svn status | grep -c "^[ACDIMRX\\!\\~]"
    p1 = subprocess.Popen(['svn', 'status'], env={"LANG": "C"}, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', '-c', '^[ACDIMR\\!\\~]'], stdin=p1.stdout, stdout=subprocess.PIPE)
    output = p2.communicate()[0].strip()
    if len(output) > 0 and int(output) > 0:
        changes = changes + ' ' + output
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG

    powerline.append(' %s ' % changes, fg, bg)

try:
    add_svn_segment()
except OSError:
    pass
except subprocess.CalledProcessError:
    pass
