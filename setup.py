#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="powerline-shell",
      version="0.1.0-alpha",
      description="A pretty prompt for your shell",
      author="Buck Ryan",
      url="httpss://github.com/banga/powerline-shell",
      classifiers=[],
      py_modules=["powerline_shell"],
      install_requires=[
          "argparse",
      ],
      entry_points="""
          [console_scripts]
          powerline-shell=powerline_shell:main
      """,
      packages=["powerline_shell"],
)
