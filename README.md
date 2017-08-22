# A Powerline style prompt for your shell

A [Powerline](https://github.com/Lokaltog/vim-powerline) like prompt for Bash,
ZSH and Fish:

![MacVim+Solarized+Powerline+CtrlP](https://raw.github.com/banga/powerline-shell/master/bash-powerline-screenshot.png)

- Shows some important details about the git/svn/hg/fossil branch (see below)
- Changes color if the last command exited with a failure code
- If you're too deep into a directory tree, shortens the displayed path with an ellipsis
- Shows the current Python [virtualenv](http://www.virtualenv.org/) environment
- It's easy to customize and extend. See below for details.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Version Control](#version-control)
- [Setup](#setup)
  - [All Shells](#all-shells)
  - [Bash](#bash)
  - [ZSH](#zsh)
  - [Fish](#fish)
- [Customization](#customization)
  - [Adding, Removing and Re-arranging segments](#adding-removing-and-re-arranging-segments)
  - [Contributing new types of segments](#contributing-new-types-of-segments)
  - [Themes](#themes)
- [Troubleshooting](#troubleshooting)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Version Control

All of the version control systems supported by powerline shell give you a
quick look into the state of your repo:

- The current branch is displayed and changes background color when the
  branch is dirty.
- When the local branch differs from the remote, the difference in number
  of commits is shown along with `⇡` or `⇣` indicating whether a git push
  or pull is pending

In addition, git has a few extra symbols:

- `✎` -- a file has been modified, but not staged for commit
- `✔` -- a file is staged for commit
- `✼` -- a file has conflicts

FIXME

- A `+` appears when untracked files are present (except for git, which uses
  `?` instead)

Each of these will have a number next to it if more than one file matches.

## Setup

This script uses ANSI color codes to display colors in a terminal. These are
notoriously non-portable, so may not work for you out of the box, but try
setting your $TERM to `xterm-256color`, because that works for me.

- Patch the font you use for your terminal: see
  [powerline-fonts](https://github.com/Lokaltog/powerline-fonts)
  - If you struggle too much to get working fonts in your terminal, you can use
    "compatible" mode.
  - If you're using old patched fonts, you have to use the older symbols.
    Basically reverse [this
    commit](https://github.com/milkbikis/powerline-shell/commit/2a84ecc) in
    your copy

- Clone this repository somewhere:

```
git clone https://github.com/milkbikis/powerline-shell
```

- Copy `config.py.dist` to `config.py` and edit it to configure the segments
  you want. Then run

```
./install.py
```

This will generate `powerline-shell.py`

- (optional) Create a symlink to this python script in your home:

```
ln -s <path/to/powerline-shell.py> ~/powerline-shell.py
```

If you don't want the symlink, just modify the path in the commands below

- For python2.6 you have to install argparse

```
pip install argparse
```

### All Shells

There are a few optional arguments which can be seen by running
`powerline-shell.py --help`.

```
  --cwd-mode {fancy,plain,dironly}
                        How to display the current directory
  --cwd-max-depth CWD_MAX_DEPTH
                        Maximum number of directories to show in path
  --cwd-max-dir-size CWD_MAX_DIR_SIZE
                        Maximum number of letters displayed for each directory
                        in the path
  --colorize-hostname   Colorize the hostname based on a hash of itself.
  --mode {patched,compatible,flat}
                        The characters used to make separators between
                        segments
```

### Bash

Add the following to your `.bashrc` (or `.profile` on Mac):

```
function _update_ps1() {
    PS1="$(~/powerline-shell.py $? 2> /dev/null)"
}

if [ "$TERM" != "linux" ]; then
    PROMPT_COMMAND="_update_ps1; $PROMPT_COMMAND"
fi
```

### ZSH

Add the following to your `.zshrc`:

```
function powerline_precmd() {
    PS1="$(~/powerline-shell.py $? --shell zsh 2> /dev/null)"
}

function install_powerline_precmd() {
  for s in "${precmd_functions[@]}"; do
    if [ "$s" = "powerline_precmd" ]; then
      return
    fi
  done
  precmd_functions+=(powerline_precmd)
}

if [ "$TERM" != "linux" ]; then
    install_powerline_precmd
fi
```

### Fish

Redefine `fish_prompt` in ~/.config/fish/config.fish:

```
function fish_prompt
    ~/powerline-shell.py $status --shell bare ^/dev/null
end
```

## Customization

### Adding, Removing and Re-arranging segments

The `config.py` file defines which segments are drawn and in which order. Simply
comment out and rearrange segment names to get your desired arrangement. Every
time you change `config.py`, run `install.py`, which will generate a new
`powerline-shell.py` customized to your configuration. You should see the new
prompt immediately.

### Contributing new types of segments

The `segments` directory contains python scripts which are injected as is into
a single file `powerline_shell_base.py`. Each segment script defines a function
that inserts one or more segments into the prompt. If you want to add a new
segment, simply create a new file in the segments directory and add its name to
the `config.py` file at the appropriate location.

Make sure that your script does not introduce new globals which might conflict
with other scripts. Your script should fail silently and run quickly in any
scenario.

Make sure you introduce new default colors in `themes/default.py` for every new
segment you create. Test your segment with this theme first.

You should add tests for your segment as best you are able. Unit and
integration tests are both welcome. Run your tests with the `nosetests` command
after install the requirements in `dev_requirements.txt`.

### Themes

The `themes` directory stores themes for your prompt, which are basically color
values used by segments. The `default.py` defines a default theme which can be
used standalone, and every other theme falls back to it if they miss colors for
any segments. Create new themes by copying any other existing theme and
changing the values. To use a theme, set the `THEME` variable in `config.py` to
the name of your theme.

A script for testing color combinations is provided at `themes/colortest.py`.
Note that the colors you see may vary depending on your terminal. When designing
a theme, please test your theme on multiple terminals, especially with default
settings.

## Troubleshooting

See the [FAQ](https://github.com/banga/powerline-shell/wiki/FAQ). If you
continue to have issues, please open an
[issue](https://github.com/banga/powerline-shell/issues/new).
