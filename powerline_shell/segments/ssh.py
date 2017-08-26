import os

def add_ssh_segment(powerline):

    if os.getenv('SSH_CLIENT'):
        powerline.append(' %s ' % powerline.network, powerline.theme.SSH_FG, powerline.theme.SSH_BG)
