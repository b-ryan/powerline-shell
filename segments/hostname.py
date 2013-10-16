def add_hostname_segment():
    if powerline.args.colorize_hostname:
        from lib.color_compliment import stringToHashToColorAndOpposite
        from lib.colortrans import rgb2short
        from socket import gethostname
        hostname = gethostname()
        FG, BG = stringToHashToColorAndOpposite(hostname)
        FG, BG = (rgb2short(*color) for color in [FG, BG])
        if powerline.args.full_hostname:
            host_prompt = hostname
        else:
            host_prompt = ' %s' % hostname.split('.')[0]

        powerline.append(host_prompt, FG, BG)
    else:
        if powerline.args.shell == 'bash':
            if powerline.args.full_hostname:
                host_prompt = ' \\H '
            else:
                host_prompt = ' \\h '
        elif powerline.args.shell == 'zsh':
            if powerline.args.full_hostname:
                host_prompt = ' %M '
            else:
                host_prompt = ' %m '
        else:
            import socket
            if powerline.args.full_hostname:
                host_prompt = ' %s ' % socket.gethostname()
            else:
                host_prompt = ' %s ' % socket.gethostname().split('.')[0]

        powerline.append(host_prompt, Color.HOSTNAME_FG, Color.HOSTNAME_BG)


add_hostname_segment()
