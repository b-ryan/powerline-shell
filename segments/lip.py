
def add_lip_segment(powerline):
    import os
        lip = ' %s ' % os.getenv('LIP')

        bgcolor = Color.USERNAME_BG

    powerline.append(lip, Color.USERNAME_FG, bgcolor)
