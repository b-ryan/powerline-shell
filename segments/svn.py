import subprocess

def add_svn_segment():
    is_svn = subprocess.Popen(['svn', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    is_svn_output = is_svn.communicate()[1].strip()
    if len(is_svn_output) != 0:
        return

    added = 0
    p1 = subprocess.Popen(['svn', 'status'], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', '-c', '^[\\?]'],
            stdin=p1.stdout, stdout=subprocess.PIPE)
    output = p2.communicate()[0].strip()
    if len(output) > 0 and int(output) > 0:
        added = output.strip()

    #"svn status | grep -c "^[ACDIMRX\\!\\~]"
    p1 = subprocess.Popen(['svn', 'status'], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', '-c', '^[ACDIMR\\!\\~]'],
            stdin=p1.stdout, stdout=subprocess.PIPE)
    output = p2.communicate()[0].strip()
    if len(output) > 0 and int(output) > 0:
        changes = u'\u0394' + output.strip()
        powerline.append(' [s] %s +%s ' % (changes, added), Color.REPO_DIRTY_FG, Color.REPO_DIRTY_BG)
    elif added:
        powerline.append(' [s] +%s ' % added, Color.REPO_CLEAN_FG, Color.REPO_CLEAN_BG)
    else:
        powerline.append(' [s] ', Color.REPO_CLEAN_FG, Color.REPO_CLEAN_BG)

try:
    add_svn_segment()
except OSError:
    pass
except subprocess.CalledProcessError:
    pass
