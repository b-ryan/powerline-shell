def add_hostname_segment():
    host_prompts = {
        'bash': ' \\h',
        'zsh': ' %m'
    }
    powerline.append(host_prompts[powerline.args.shell], 250, 238)
