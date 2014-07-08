import os

# This segment displays the current chroot
# if you are in one
def add_chroot_segment():
    cwd = powerline.cwd or os.getenv('PWD')
    chroot = os.getenv('SMSCHROOT')
    if (chroot):
        powerline.append( u' \u27a5 %s ' % os.path.basename(chroot), Color.CHROOT_FG, Color.CHROOT_BG)

add_chroot_segment()
