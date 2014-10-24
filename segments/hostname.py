def add_hostname_segment():
    if powerline.args.colorize_hostname:
        from lib.color_compliment import string_to_hash_to_color_and_opposite
        from lib.colortrans import rgb2short
        from socket import gethostname
        hostname = gethostname()
        fg, bg = string_to_hash_to_color_and_opposite(hostname)
        fg, bg = (rgb2short(*color) for color in [fg, bg])
        host_prompt = ' %s ' % hostname.split('.')[0]

        powerline.append(host_prompt, fg, bg)
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
