import subprocess


def add_npm_version_segment(powerline):
    try:
        p1 = subprocess.Popen(["npm", "--version"], stdout=subprocess.PIPE)
        version = p1.communicate()[0].decode("utf-8").rstrip()
        version = "npm " + version
        powerline.append(version, 15, 18)
    except OSError:
        return
