Powerline style prompt for Bash and ZSH.
==============================================

A [Powerline](https://github.com/Lokaltog/vim-powerline) like prompt for Bash/ZSH in 2 lines:

![Screenshot](https://f.cloud.github.com/assets/1036439/72699/d4252786-601e-11e2-85e6-782868ffeeb9.png)

*  Split in 2 lines
*  Shows date/time
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

        git clone https://github.com/Janhouse/powerline-shell

* Create a symlink to the python script in your home:

        ln -s <path/to/powerline-shell.py> ~/.powerline-shell.py

  If you don't want the symlink, just modify the path in the commands below

* Now add the following to your .bashrc:

        CHROOT=`ls -di / | awk '{if ($1 != "2") print 1; else print 0;}'`
        function _update_ps1() {
            if [ "$TERM" != "linux" ] ; then
                PREV=$?
                EXTRA=`logname`@`hostname`
                export PS1="$(~/.powerline-shell.py ${PREV} --width ${COLUMNS} --chroot ${CHROOT} --extra ${EXTRA})"
            fi
        }

        export PROMPT_COMMAND="_update_ps1"

* ZSH fans, add the following to your .zshrc:

        CHROOT=`ls -di / | awk '{if ($1 != "2") print 1; else print 0;}'`
        function powerline_precmd() {
            PREV=$?
            EXTRA=`logname`@`hostname`
            export PS1="$(~/.powerline-shell.py ${PREV} --width ${COLUMNS} --chroot ${CHROOT} --shell zsh --extra ${EXTRA})"
        }

        function install_powerline_precmd() {
          for s in "${precmd_functions[@]}"; do
            if [ "$s" = "powerline_precmd" ]; then
              return
            fi
          done
          precmd_functions+=(powerline_precmd)
        }
        if [ "$TERM" != "linux" ] ; then
            install_powerline_precmd
        else
            prompt walters
        fi

* Fish users, redefine `fish_prompt` in ~/.config/fish/config.fish:

        function fish_prompt
            ~/.powerline-shell.py $status --width ${COLUMNS} --shell bare
        end
