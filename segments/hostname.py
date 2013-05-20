def add_hostname_segment():
    if powerline.args.shell == 'bash':
        host_prompt = ' \\h'
    elif powerline.args.shell == 'zsh':
        host_prompt = ' %m'
    else:
        import socket
        host_prompt = ' %s' % socket.gethostname().split('.')[0]

    powerline.append(host_prompt, Color.HOSTNAME_FG, Color.HOSTNAME_BG)

add_hostname_segment()
