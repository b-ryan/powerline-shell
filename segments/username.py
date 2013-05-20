
def add_username_segment():
    if powerline.args.shell == 'bash':
        user_prompt = ' \\u'
    elif powerline.args.shell == 'zsh':
        user_prompt = ' %n'
    else:
        import os
        user_prompt = ' %s' % os.getenv('USER')

    powerline.append(user_prompt, Color.USERNAME_FG, Color.USERNAME_BG)

add_username_segment()
