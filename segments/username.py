
def add_username_segment():
    if powerline.args.shell == 'bash':
        user_prompt = ' \\u '
    elif powerline.args.shell == 'zsh':
        user_prompt = ' %n '
    else:
        import os
        user_prompt = ' %s ' % os.getenv('USER')

    if os.getenv('USER') == 'root':
        bgcolor = Color.USERNAME_ROOT_BG
    else:
        bgcolor = Color.USERNAME_BG

    powerline.append(user_prompt, Color.USERNAME_FG, bgcolor)

add_username_segment()
