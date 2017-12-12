# A Powerline style prompt for your shell

A [Powerline](https://github.com/Lokaltog/vim-powerline) like prompt for Bash,
ZSH, Fish, and tcsh:

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
  - [Bash](#bash)
  - [ZSH](#zsh)
  - [Fish](#fish)
- [Customization](#customization)
  - [Config File](#config-file)
  - [Adding, Removing and Re-arranging segments](#adding-removing-and-re-arranging-segments)
  - [Segment Separator](#segment-separator)
  - [Themes](#themes)
  - [Segment Configuration](#segment-configuration)
  - [Contributing new types of segments](#contributing-new-types-of-segments)
- [Troubleshooting](#troubleshooting)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Version Control

All of the version control systems supported by powerline shell give you a
quick look into the state of your repo:

- The current branch is displayed and changes background color when the
  branch is dirty.
- When the local branch differs from the remote, the difference in number
  of commits is shown along with `⇡` or `⇣` indicating whether a git push
  or pull is pending.

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
    your copy.

- Install using pip:

```
pip install powerline-shell
```

(*You can use the
[`--user`](https://pip.pypa.io/en/stable/user_guide/#user-installs) option to
install for just your user, if you'd like. But you may need to fiddle with your
`PATH` to get this working properly.*)

- Or, install from the git repository:

```
git clone https://github.com/banga/powerline-shell
cd powerline-shell
python setup.py install
```

- Setup your shell prompt using the instructions for your shell below.

### Bash

Add the following to your `.bashrc` (or `.profile` on Mac):

```
function _update_ps1() {
    PS1="$(powerline-shell $?)"
}

if [ "$TERM" != "linux" ]; then
    PROMPT_COMMAND="_update_ps1; $PROMPT_COMMAND"
fi
```

### ZSH

Add the following to your `.zshrc`:

```
function powerline_precmd() {
    PS1="$(powerline-shell --shell zsh $?)"
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
    powerline-shell --shell bare $status
end
```

### tcsh

Add the following to your `.tcshrc`:

```
alias precmd 'set prompt="`powerline-shell --shell tcsh $?`"'
```

## Customization

### Config File

Powerline-shell is customizable through the use of a config file. This file is
expected to be located at `~/.powerline-shell.json`. You can generate the
default config at this location using:

```
powerline-shell --generate-config > ~/.powerline-shell.json
```

(You can see an example config file
[here](https://github.com/b-ryan/dotfiles/blob/master/home/powerline-shell.json))

### Adding, Removing and Re-arranging segments

Once you have generated your config file, you can now start adding or removing
"segments" - the building blocks of your shell. The list of segments available
are:

- `aws_profile` - Show which AWS profile is in use. See the
  [AWS](http://docs.aws.amazon.com/cli/latest/userguide/cli-multiple-profiles.html)
  documentation.
- `battery` - See percentage of battery charged and an icon when the battery is
  charging.
- `bzr` - Details about the current Bazaar repo.
- `cwd` - Shows your current working directory. See [Segment
  Configuration](#segment-configuration) for some options.
- `exit_code` - When the previous command ends in a non-zero status, shows the
  value of the exit status in red.
- `fossil` - Details about the current Fossil repo.
- `git` - Details about the current Git repo.
- `hg` - Details about the current Mercurial repo.
- `hostname` - Current machine's hostname.
- `jobs` - Number of background jobs currently running.
- `newline` - Inserts a newline into the prompt.
- `node_version` - `node --version`
- `npm_version` - `npm --version`
- `php_version` - Version of php on the machine.
- `rbenv` - `rbenv local`
- `read_only` - Shows a lock icon if the current directory is read-only.
- `root` - Shows a `#` if logged in as root, `$` otherwise.
- `ruby_version` - `ruby --version`
- `set_term_title` - If able, sets the title of your terminal to include some
  useful info.
- `ssh` - If logged into over SSH, shows a network icon.
- `svn` - Details about the current SVN repo.
- `time` - Shows the current time.
- `uptime` - Uptime of the current machine.
- `username` - Name of the logged-in user.
- `virtual_env` - Shows the name of the current virtual env or conda env.

### Segment Separator

By default, a unicode character (resembling the > symbol) is used to separate
each segment. This can be changed by changing the "mode" option in the config
file. The available modes are:

- `patched` - The default.
- `compatible` - Attempts to use characters that may already be available using
  your chosen font.
- `flat` - No separator is used between segments, giving each segment a
  rectangular appearance (and also saves space).

### Themes

The `powerline_shell/themes` directory stores themes for your prompt, which are
basically color values used by segments. The `default.py` defines a default
theme which can be used standalone, and every other theme falls back to it if
they miss colors for any segments. Create new themes by copying any other
existing theme and changing the values. To use a theme, set the `theme`
variable in `~/.powerline-shell.json` to the name of your theme.

A script for testing color combinations is provided at `colortest.py`. Note
that the colors you see may vary depending on your terminal. When designing a
theme, please test your theme on multiple terminals, especially with default
settings.

### Segment Configuration

Some segments support additional configuration. The options for the segment are
nested under the name of the segment itself. For example, all of the options
for the `cwd` segment are set in `~/.powerline-shell.py` like:

```
{
    "segments": [...],
    "cwd": {
        options go here
    }
}
```

The options for the `cwd` segment are:

- `mode`: If "plain" then simple text will be used to show the cwd. If
  "dironly," only the current directory will be shown. Otherwise expands the
  cwd into individual directories.
- `max_depth`: Maximum number of directories to show in path.
- `max_dir_size`: Maximum number of characters displayed for each directory in
  the path.
- `full_cwd`: If true, the last directory will not be shortened when
  `max_dir_size` is used.

The `hostname` segment provides one option:

- `colorize`: If true, the hostname will be colorized based on a hash of
  itself.

The options for the `battery` segment are:

- `always_show_percentage`: If true, show percentage when fully charged on AC.
- `low_threshold`: Threshold percentage for low-battery indicator color.

### Contributing new types of segments

The `powerline_shell/segments` directory contains python scripts which are
injected as is into a single file `powerline_shell_base.py`. Each segment
script defines a function that inserts one or more segments into the prompt. If
you want to add a new segment, simply create a new file in the segments
directory.

Make sure that your script does not introduce new globals which might conflict
with other scripts. Your script should fail silently and run quickly in any
scenario.

Make sure you introduce new default colors in `themes/default.py` for every new
segment you create. Test your segment with this theme first.

You should add tests for your segment as best you are able. Unit and
integration tests are both welcome. Run your tests by running the `test.sh`
script. It uses `docker` to manage dependencies and the environment.
Alternatively, you can run the `nosetests` command after installing the
requirements in `requirements-dev.txt`.

## Troubleshooting

See the [FAQ](https://github.com/banga/powerline-shell/wiki/FAQ). If you
continue to have issues, please open an
[issue](https://github.com/banga/powerline-shell/issues/new).
