def add_exit_code_segment(powerline):
    if powerline.args.prev_error == 0:
        return
    fg = powerline.theme.CMD_FAILED_FG
    bg = powerline.theme.CMD_FAILED_BG
    powerline.append(' %s ' % str(powerline.args.prev_error), fg, bg)
