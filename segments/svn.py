import subprocess


def _add_svn_segment(powerline):
    is_svn = subprocess.Popen(['svn', 'status'],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    is_svn_output = is_svn.communicate()[1].decode("utf-8").strip()
    if len(is_svn_output) != 0:
        return

    #"svn status | grep -c "^[ACDIMRX\\!\\~]"
    p1 = subprocess.Popen(['svn', 'status'], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', '-c', '^[ACDIMR\\!\\~]'],
            stdin=p1.stdout, stdout=subprocess.PIPE)
    output = p2.communicate()[0].decode("utf-8").strip()
    if len(output) > 0 and int(output) > 0:
        changes = output.strip()
        powerline.append(' %s ' % changes, Color.SVN_CHANGES_FG, Color.SVN_CHANGES_BG)


def add_svn_segment(powerline):
    """Wraps _add_svn_segment in exception handling."""

    # FIXME This function was added when introducing a testing framework,
    # during which the 'powerline' object was passed into the
    # `add_[segment]_segment` functions instead of being a global variable. At
    # that time it was unclear whether the below exceptions could actually be
    # thrown. It would be preferable to find out whether they ever will. If so,
    # write a comment explaining when. Otherwise remove.

    try:
        _add_svn_segment(powerline)
    except OSError:
        pass
    except subprocess.CalledProcessError:
        pass
