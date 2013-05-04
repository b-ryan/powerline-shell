def add_hostname_segment():
    host_prompts = {
        'bash': ' \\h',
        'zsh': ' %m'
    }
    powerline.append(host_prompts[powerline.args.shell], Color.HOSTNAME_FG,
            Color.HOSTNAME_BG)

add_hostname_segment()
