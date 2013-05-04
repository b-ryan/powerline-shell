def add_username_segment():
    user_prompts = {
        'bash': ' \\u',
        'zsh': ' %n'
    }
    powerline.append(user_prompts[powerline.args.shell], 250, 240)

add_username_segment()
