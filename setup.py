#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="powerline-shell",
    version="0.7.0",
    description="A pretty prompt for your shell",
    author="Buck Ryan",
    author_email="buck@buckryan.com",
    license="MIT",
    url="https://github.com/b-ryan/powerline-shell",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
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
