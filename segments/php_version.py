import subprocess


def add_php_version_segment():
    try:
        version = ' %s ' % subprocess.check_output(['php', '-r', 'echo PHP_VERSION;'], stderr=subprocess.STDOUT)
        powerline.append(version, 15, 4)
    except OSError:
        return

add_php_version_segment()
