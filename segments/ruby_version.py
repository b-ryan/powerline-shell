import subprocess


def add_ruby_version_segment():
    try:
        p1 = subprocess.Popen(["ruby", "-v"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["sed", "s/ (.*//"], stdin=p1.stdout, stdout=subprocess.PIPE)
        version = p2.communicate()[0].rstrip()
        powerline.append(version, 15, 1)
    except OSError:
        return

add_ruby_version_segment()
