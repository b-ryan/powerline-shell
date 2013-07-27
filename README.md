A Powerline style prompt for your shell
=======================================

A [Powerline](https://github.com/Lokaltog/vim-powerline) like prompt for Bash, ZSH and Fish:

![MacVim+Solarized+Powerline+CtrlP](https://raw.github.com/milkbikis/dotfiles-mac/master/bash-powerline-screenshot.png)

*  Shows some important details about the git/svn/hg/fossil branch:
    *  Displays the current branch which changes background color when the branch is dirty
    *  A '+' appears when untracked files are present
    *  When the local branch differs from the remote, the difference in number of commits is shown along with '⇡' or '⇣' indicating whether a git push or pull is pending
*  Changes color if the last command exited with a failure code
*  If you're too deep into a directory tree, shortens the displayed path with an ellipsis
*  Shows the current Python [virtualenv](http://www.virtualenv.org/) environment
*  It's easy to customize and extend. See below for details.

# Setup

This script uses ANSI color codes to display colors in a terminal. These are
notoriously non-portable, so may not work for you out of the box, but try 
setting your $TERM to xterm-256color, because that works for me.

* Patch the font you use for your terminal: see https://github.com/Lokaltog/vim-powerline/wiki/Patched-fonts

  * If you struggle too much to get working fonts in your terminal, you can use "compatible" mode.

* Clone this repository somewhere:

        git clone https://github.com/milkbikis/powerline-shell

* Configure the segments you want by editing `config.py`. Then run

        ./install.py

  * This will generate `powerline-shell.py`

* (optional) Create a symlink to this python script in your home:

        ln -s <path/to/powerline-shell.py> ~/powerline-shell.py

  * If you don't want the symlink, just modify the path in the commands below

* For python2.6 you have to install argparse

        pip install argparse

### All Shells:
There are a few optional arguments which can be seen by running `powerline-shell.py --help`.

```
  --cwd-only            Only show the current directory
  --cwd-max-depth CWD_MAX_DEPTH
                        Maximum number of directories to show in path
  --colorize-hostname   Colorize the hostname based on a hash of itself.
  --mode {patched,compatible,flat}
                        The characters used to make separators between
                        segments
```

### Bash:
Add the following to your `.bashrc`:

        function _update_ps1() {
           export PS1="$(~/powerline-shell.py $?)"
        }

        export PROMPT_COMMAND="_update_ps1"

### ZSH:
Add the following to your `.zshrc`:

        function powerline_precmd() {
          export PS1="$(~/powerline-shell.py $? --shell zsh)"
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

### Fish:
Redefine `fish_prompt` in ~/.config/fish/config.fish:

        function fish_prompt
            ~/powerline-shell.py $status --shell bare
        end

# Customization

### Adding, Removing and Re-arranging segments

The `config.py` file defines which segments are drawn and in which order. Simply
comment out and rearrange segment names to get your desired arrangement. Every
time you change `config.py`, run `install.py`, which will generate a new
`powerline-shell.py` customized to your configuration. You should see the new
prompt immediately.

### Contributing new types of segments

The `segments` directory contains python scripts which are injected as is into
a single file `powerline-shell.py.template`. Each segment script defines a 
function that inserts one or more segments into the prompt. If you want to add a
new segment, simply create a new file in the segments directory and add its name
to the `config.py` file at the appropriate location.

Make sure that your script does not introduce new globals which might conflict 
with other scripts. Your script should fail silently and run quickly in any
scenario.

### Themes

The `themes` directory stores themes for your prompt, which are basically color
values used by segments. Create a new theme by copying `themes/default.py` and
changing the values. To use a theme, set the `THEME` variable in `config.py` to
the name of your theme.

A script for testing color combinations is provided at `themes/colortest.py`.
Note that the colors you see may vary depending on your terminal. When designing
a theme, please test your theme on multiple terminals, especially with default
settings.
