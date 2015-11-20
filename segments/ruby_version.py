import subprocess


def add_ruby_version_segment(powerline):
    try:
        p1 = subprocess.Popen(["ruby", "-v"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["sed", "s/ (.*//"], stdin=p1.stdout, stdout=subprocess.PIPE)
        version = p2.communicate()[0].decode("utf-8").rstrip()
        if os.environ.has_key("GEM_HOME"):
          gem = os.environ["GEM_HOME"].split("@")
          if len(gem) > 1:
            version += " " + gem[1]
        powerline.append(version, 15, 1)
    except OSError:
        return
