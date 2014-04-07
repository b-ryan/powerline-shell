import subprocess


def add_ruby_version_segment():
    try:
        p1 = subprocess.Popen(["rbenv", "global"], stdout=subprocess.PIPE)
        version = p1.communicate()[0].rstrip()
        powerline.append(version, 15, 1)
    except OSError:
        return

add_ruby_version_segment()
