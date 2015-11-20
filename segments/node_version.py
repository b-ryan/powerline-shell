import subprocess


def add_node_version_segment():
    try:
        p1 = subprocess.Popen(["node", "--version"], stdout=subprocess.PIPE)
        version = p1.communicate()[0].decode("utf-8").rstrip()
        version = "node " + version
        powerline.append(version, 15, 18)
    except OSError:
        return

add_node_version_segment()
