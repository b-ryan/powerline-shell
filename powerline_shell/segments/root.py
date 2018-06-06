from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        config = self.powerline.config

        def exists(obj, chain):
            _key = chain.pop(0)
            if _key in obj:
                return exists(obj[_key], chain) if chain else obj[_key]

        def indicators(default, shell, path='root.indicators'):
            indicator = exists(config, (path + '.' + shell).split('.'))
            return indicator if indicator else default

        root_indicators = {
            'bash': indicators(' \\$ ', 'bash'),
            'tcsh': indicators(' %# ', 'tcsh'),
            'zsh': indicators(' %# ', 'zsh'),
            'bare': indicators(' $ ', 'bare'),
        }
        bg = powerline.theme.CMD_PASSED_BG
        fg = powerline.theme.CMD_PASSED_FG
        if powerline.args.prev_error != 0:
            fg = powerline.theme.CMD_FAILED_FG
            bg = powerline.theme.CMD_FAILED_BG
        powerline.append(root_indicators[powerline.args.shell], fg, bg, sanitize=False)
