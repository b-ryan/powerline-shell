def add_status_indicator_segment():
    if powerline.args.prev_error == 0:
        return
    fg = Color.CMD_FAILED_FG
    bg = Color.CMD_FAILED_BG
    powerline.append(str(powerline.args.prev_error), fg, bg)

add_status_indicator_segment()
