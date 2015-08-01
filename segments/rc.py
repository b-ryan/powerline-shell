def add_rc_indicator_segment():
    if powerline.args.prev_error != 0:
        fg = Color.CMD_FAILED_FG
        bg = Color.CMD_FAILED_BG
        text = '%d' % (powerline.args.prev_error)
        powerline.append(text, fg, bg)

add_rc_indicator_segment()
