def add_hostname_segment():
    from lib.color_compliment import stringToHashToColorAndOpposite
    from lib.colortrans import rgb2short
    from socket import gethostname
    hostname = gethostname()
    FG, BG = stringToHashToColorAndOpposite(hostname)
    FG, BG = (rgb2short(*color) for color in [FG, BG])
    host_prompt = ' %s' % hostname.split('.')[0]

    powerline.append(host_prompt, FG, BG)

add_hostname_segment()
