import os

def add_ruby_gemset_segment():
    if not os.path.isfile(".ruby-version"):
        return

    with open(".ruby-version") as f:
        ruby_version = f.read().rstrip()

    if os.path.isfile(".ruby-gemset"):
        with open(".ruby-gemset") as f:
            ruby_gemset = f.read().rstrip()
        ruby_version = ruby_version + "@" + ruby_gemset

    bg = Color.VIRTUAL_ENV_BG
    fg = Color.VIRTUAL_ENV_FG
    powerline.append(' %s ' % ruby_version, fg, bg)

add_ruby_gemset_segment()
