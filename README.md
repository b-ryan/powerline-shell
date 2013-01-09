Powerline style prompt for Bash (and now, ZSH)
==============================================

A [Powerline](https://github.com/Lokaltog/vim-powerline) like prompt for Bash/ZSH:

![MacVim+Solarized+Powerline+CtrlP](https://raw.github.com/milkbikis/dotfiles-mac/master/bash-powerline-screenshot.png)

*  Shows some important details about the git branch:
    *  Displays the current git branch which changes background color when the branch is dirty
    *  A '+' appears when untracked files are present
    *  When the local branch differs from the remote, the difference in number of commits is shown along with '⇡' or '⇣' indicating whether a git push or pull is pending
*  Changes color if the last command exited with a failure code
*  If you're too deep into a directory tree, shortens the displayed path with an ellipsis
*  Shows the current Python [virtualenv](http://www.virtualenv.org/) environment
*  It's all done in a Python script, so you could go nuts with it

# Setup

* This script uses ANSI color codes to display colors in a terminal. These are notoriously non-portable, so may not work for you out of the box, but try setting your $TERM to xterm-256color, because that works for me.

* Patch the font you use for your terminal: see https://github.com/Lokaltog/vim-powerline/wiki/Patched-fonts

* Clone this repository somewhere:

        git clone https://github.com/milkbikis/powerline-bash

* Create a symlink to the python script in your home:

        ln -s <path/to/powerline-bash.py> ~/powerline-bash.py

  If you don't want the symlink, just modify the path in the commands below

* Now add the following to your .bashrc:

        function _update_ps1() {
           export PS1="$(~/powerline-bash.py $?)"
        }

        export PROMPT_COMMAND="_update_ps1"

* ZSH fans, add the following to your .zshrc:

        function powerline_precmd() {
          export PS1="$(~/powerline-bash.py $? --shell zsh)"
        }

        function install_powerline_precmd() {
          for s in "${precmd_functions[@]}"; do
            if [ "$s" = "powerline_precmd" ]; then
              return
            fi
          done
          precmd_functions+=(powerline_precmd)
        }

        install_powerline_precmd

* Fish users, redefine `fish_prompt` in ~/.config/fish/config.fish:

        function fish_prompt
            ~/powerline-bash.py $status --shell bare
        end
