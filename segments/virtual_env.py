import os

def add_virtual_env_segment(powerline):
    env = os.getenv('VIRTUAL_ENV') or os.getenv('CONDA_ENV_PATH')
    if env is None:
        return

    env_name = os.path.basename(env)
    bg = Color.VIRTUAL_ENV_BG
    fg = Color.VIRTUAL_ENV_FG
    env_name_mod = u" \U0001F40D  {} ".format(env_name)
    powerline.append(env_name_mod, fg, bg)
