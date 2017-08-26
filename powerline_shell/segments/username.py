
def add_username_segment(powerline):
    import os
    if powerline.args.shell == 'bash':
        user_prompt = ' \\u '
    elif powerline.args.shell == 'zsh':
        user_prompt = ' %n '
    else:
        user_prompt = ' %s ' % os.getenv('USER')

    if os.getenv('USER') == 'root':
        bgcolor = powerline.theme.USERNAME_ROOT_BG
    else:
        bgcolor = powerline.theme.USERNAME_BG

    powerline.append(user_prompt, powerline.theme.USERNAME_FG, bgcolor)
