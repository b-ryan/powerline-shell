import subprocess


def add_php_version_segment():
    try:
        version = ' %s ' % subprocess.check_output(['ruby', '-e', 'print RUBY_VERSION'], stderr=subprocess.STDOUT)
        powerline.append(version, 15, 1)
    except OSError:
        return

add_php_version_segment()
