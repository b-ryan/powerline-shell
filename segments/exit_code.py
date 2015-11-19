def add_exit_code_segment():
    if powerline.args.prev_error == 0:
        return
    fg = Color.CMD_FAILED_FG
    bg = Color.CMD_FAILED_BG
    powerline.append(' %s ' % str(powerline.args.prev_error), fg, bg)

add_exit_code_segment()
