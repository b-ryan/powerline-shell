def add_exit_indicator_segment():
    exit_code = powerline.args.prev_error

    if not exit_code:
        return

    fg = Color.CMD_FAILED_FG
    bg = Color.CMD_FAILED_BG

    indicator = " {} ".format(exit_code)
    powerline.append(indicator, fg, bg)

add_exit_indicator_segment()
