import os

def add_ssh_segment(powerline):

    if os.getenv('SSH_CLIENT'):
        powerline.append(' %s ' % powerline.network, Color.SSH_FG, Color.SSH_BG)
