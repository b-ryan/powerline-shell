#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="powerline-shell",
    version="0.4.3",
    description="A pretty prompt for your shell",
    author="Buck Ryan",
    url="https://github.com/banga/powerline-shell",
    classifiers=[],
    packages=[
        "powerline_shell",
        "powerline_shell.segments",
        "powerline_shell.themes",
    ],
    install_requires=[
        "argparse",
    ],
    entry_points="""
    [console_scripts]
    powerline-shell=powerline_shell:main
    """,
)
