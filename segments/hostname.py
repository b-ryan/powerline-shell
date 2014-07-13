def get_colors_for_hostname(hostname):
    cmin = 17    # min ANSI color to use
    cmax = 231   # max ANSI color to use
    white_fg = ( # color ranges that should use white FG
        range(16,34), range(52,70), range(88,106), 
        range(124,136), range(160,172), range(196,208)
    )

    crange = cmax - cmin + 1
    bg = (hash(hostname) % crange) + cmin
    fg = 7 if (True in [bg in r for r in white_fg]) else 8
    return (fg,bg)

def add_hostname_segment():
    if powerline.args.colorize_hostname:
        from socket import gethostname
        hostname = gethostname()
        FG, BG = get_colors_for_hostname(hostname)
        host_prompt = ' %s ' % hostname.split('.')[0]

        powerline.append(host_prompt, FG, BG)
    else:
        if powerline.args.shell == 'bash':
            host_prompt = ' \\h '
        elif powerline.args.shell == 'zsh':
            host_prompt = ' %m '
        else:
            import socket
            host_prompt = ' %s ' % socket.gethostname().split('.')[0]

        powerline.append(host_prompt, Color.HOSTNAME_FG, Color.HOSTNAME_BG)


add_hostname_segment()
