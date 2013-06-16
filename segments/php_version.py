import subprocess


def add_php_version_segment():
    try:
        version = ' %s ' % subprocess.check_output(['php', '--version'], stderr=subprocess.STDOUT).split(' ')[1]
        powerline.append(version, 15, 4)
    except OSError:
        return

add_php_version_segment()
