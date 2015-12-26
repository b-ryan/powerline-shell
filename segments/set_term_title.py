def add_set_term_title_segment(powerline):
    term = os.getenv('TERM')
    if not (('xterm' in term) or ('rxvt' in term)):
        return

    if powerline.args.shell == 'bash':
        set_title = '\\[\\e]0;\\u@\\h: \\w\\a\\]'
    elif powerline.args.shell == 'zsh':
        set_title = '\033]0;%n@%m: %~\007'
    else:
        import socket
        set_title = '\033]0;%s@%s: %s\007' % (os.getenv('USER'), socket.gethostname().split('.')[0], powerline.cwd or os.getenv('PWD'))

    powerline.append(set_title, None, None, '')

