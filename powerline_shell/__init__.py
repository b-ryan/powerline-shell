#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import os
import sys
import importlib
import json
from .utils import warn, py3
import re


def get_valid_cwd():
    """ We check if the current working directory is valid or not. Typically
        happens when you checkout a different branch on git that doesn't have
        this directory.
        We return the original cwd because the shell still considers that to be
        the working directory, so returning our guess will confuse people
    """
    # Prefer the PWD environment variable. Python's os.getcwd function follows
    # symbolic links, which is undesirable. But if PWD is not set then fall
    # back to this func
    try:
        cwd = os.getenv('PWD') or os.getcwd()
    except:
        warn("Your current directory is invalid. If you open a ticket at " +
            "https://github.com/milkbikis/powerline-shell/issues/new " +
            "we would love to help fix the issue.")
        sys.stdout.write("> ")
        sys.exit(1)

    parts = cwd.split(os.sep)
    up = cwd
    while parts and not os.path.exists(up):
        parts.pop()
        up = os.sep.join(parts)
    if cwd != up:
        warn("Your current directory is invalid. Lowest valid directory: "
            + up)
    return cwd


class Powerline(object):
    symbols = {
        'compatible': {
            'lock': 'RO',
            'network': 'SSH',
            'separator': u'\u25B6',
            'separator_thin': u'\u276F'
        },
        'patched': {
            'lock': u'\uE0A2',
            'network': 'SSH',
            'separator': u'\uE0B0',
            'separator_thin': u'\uE0B1'
        },
        'flat': {
            'lock': u'\uE0A2',
            'network': 'SSH',
            'separator': '',
            'separator_thin': ''
        },
    }

    color_templates = {
        'bash': r'\[\e%s\]',
        'tcsh': r'%%{\e%s%%}',
        'zsh': '%%{%s%%}',
        'bare': '%s',
    }

    def __init__(self, args, config, theme):
        self.args = args
        self.config = config
        self.theme = theme
        self.cwd = get_valid_cwd()
        mode = config.get("mode", "patched")
        self.color_template = self.color_templates[args.shell]
        self.reset = self.color_template % '[0m'
        self.lock = Powerline.symbols[mode]['lock']
        self.network = Powerline.symbols[mode]['network']
        self.separator = Powerline.symbols[mode]['separator']
        self.separator_thin = Powerline.symbols[mode]['separator_thin']
        self.segments = []

    def segment_conf(self, seg_name, key, default=None):
        return self.config.get(seg_name, {}).get(key, default)

    def color(self, prefix, code):
        if code is None:
            return ''
        elif code == self.theme.RESET:
            return self.reset
        else:
            return self.color_template % ('[%s;5;%sm' % (prefix, code))

    def fgcolor(self, code):
        return self.color('38', code)

    def bgcolor(self, code):
        return self.color('48', code)

    def append(self, content, fg, bg, separator=None, separator_fg=None):
        self.segments.append((content, fg, bg,
            separator if separator is not None else self.separator,
            separator_fg if separator_fg is not None else bg))

    def draw(self):
        text = (''.join(self.draw_segment(i) for i in range(len(self.segments)))
                + self.reset) + ' '
        if py3:
            return text
        else:
            return text.encode('utf-8')

    def draw_segment(self, idx):
        segment = self.segments[idx]
        if self.args.shell == "bash":
            sanitized = re.sub(r"([`$])", r"\\\1", segment[0])
        else:
            sanitized = segment[0]
        next_segment = self.segments[idx + 1] if idx < len(self.segments)-1 else None

        return ''.join((
            self.fgcolor(segment[1]),
            self.bgcolor(segment[2]),
            sanitized,
            self.bgcolor(next_segment[2]) if next_segment else self.reset,
            self.fgcolor(segment[4]),
            segment[3]))


def find_config():
    for location in [
        "powerline-shell.json",
        "~/.powerline-shell.json",
    ]:
        full = os.path.expanduser(location)
        if os.path.exists(full):
            return full

DEFAULT_CONFIG = {
    "segments": [
        'virtual_env',
        'username',
        'hostname',
        'ssh',
        'cwd',
        'git',
        'hg',
        'jobs',
        'root',
    ]
}


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--generate-config', action='store_true',
                            help='Generate the default config and print it to stdout')
    arg_parser.add_argument('--shell', action='store', default='bash',
                            help='Set this to your shell type',
                            choices=['bash', 'tcsh', 'zsh', 'bare'])
    arg_parser.add_argument('prev_error', nargs='?', type=int, default=0,
                            help='Error code returned by the last command')
    args = arg_parser.parse_args()

    if args.generate_config:
        print(json.dumps(DEFAULT_CONFIG, indent=2))
        return 0

    config_path = find_config()
    if config_path:
        with open(config_path) as f:
            config = json.loads(f.read())
    else:
        config = DEFAULT_CONFIG

    theme_name = config.get("theme", "default")
    mod = importlib.import_module("powerline_shell.themes." + theme_name)
    theme = getattr(mod, "Color")

    powerline = Powerline(args, config, theme)
    segments = []
    for seg_name in config["segments"]:
        mod = importlib.import_module("powerline_shell.segments." + seg_name)
        segment = getattr(mod, "Segment")(powerline)
        segment.start()
        segments.append(segment)
    for segment in segments:
        segment.add_to_powerline()
    sys.stdout.write(powerline.draw())
    return 0
