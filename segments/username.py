def add_username_segment():
    user_prompts = {
        'bash': ' \\u',
        'zsh': ' %n'
    }
    powerline.append(user_prompts[powerline.args.shell], Color.USERNAME_FG,
            Color.USERNAME_BG)

add_username_segment()
