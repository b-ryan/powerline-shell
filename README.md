Powerline style prompt for Bash
===============================

I implemented a [Powerline](https://github.com/Lokaltog/vim-powerline) like prompt for Bash:

![MacVim+Solarized+Powerline+CtrlP](https://raw.github.com/milkbikis/dotfiles-mac/master/bash-powerline-screenshot.png)

*  Displays the current git branch
*  Changes color if the last command exited with a failure code
*  It's all done in a Python script, so you could go nuts with it

# Setup

* This script uses ANSI color codes to display colors in a terminal. These are notoriously non-portable, so may not work for you out of the box, but try setting your $TERM to xterm-256color, because that works for me.

* Patch the font you use for your terminal: see https://github.com/Lokaltog/vim-powerline/wiki/Patched-fonts

* Clone this repository somewhere:

        git clone https://github.com/milkbikis/powerline-bash

* Create a symlink to the python script in your home:

        ln -s <path/to/powerline-bash.py> ~/powerline-bash.py

  If you don't want the symlink, just modify the path in the .bashrc command below

* Now add the following to your .bashrc:

        function _update_ps1()
        {
           export PS1="$(~/powerline-bash.py $?)"
        }

        export PROMPT_COMMAND="_update_ps1"
