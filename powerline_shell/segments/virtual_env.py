import os
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        env = os.getenv('VIRTUAL_ENV') \
            or os.getenv('CONDA_ENV_PATH') \
            or os.getenv('CONDA_DEFAULT_ENV')
        if os.getenv('VIRTUAL_ENV') \
            and os.path.basename(env) == '.venv':
            env = os.path.basename(os.path.dirname(env))
        if not env:
            return
        env_name = os.path.basename(env)
        bg = self.powerline.theme.VIRTUAL_ENV_BG
        fg = self.powerline.theme.VIRTUAL_ENV_FG
        self.powerline.append(" " + env_name + " ", fg, bg)
