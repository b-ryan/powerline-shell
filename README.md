# A Powerline style prompt for your shell

A beautiful and useful prompt generator for Bash, ZSH, Fish, and tcsh:

![MacVim+Solarized+Powerline+CtrlP](https://raw.github.com/b-ryan/powerline-shell/master/bash-powerline-screenshot.png)

- Shows some important details about the git/svn/hg/fossil branch (see below)
- Changes color if the last command exited with a failure code
- If you're too deep into a directory tree, shortens the displayed path with an ellipsis
- Shows the current Python [virtualenv](http://www.virtualenv.org/) environment
- It's easy to customize and extend. See below for details.

The generated prompts are designed to resemble
[powerline](https://github.com/powerline/powerline), but otherwise this project
has no relation to powerline.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Version Control](#version-control)
- [Setup](#setup)
  - [Bash](#bash)
  - [ZSH](#zsh)
  - [Fish](#fish)
  - [tcsh](#tcsh)
- [Customization](#customization)
  - [Config File](#config-file)
  - [Adding, Removing and Re-arranging segments](#adding-removing-and-re-arranging-segments)
  - [Generic Segments](#generic-segments)
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

If files are modified or in conflict, the situation is summarized with the
following symbols:

- `✎` -- a file has been modified (but not staged for commit, in git)
- `✔` -- a file is staged for commit (git) or added for tracking
- `✼` -- a file has conflicts
- `?` -- a file is untracked

Each of these will have a number next to it if more than one file matches.

The segment can start with a symbol representing the version control system in
use. To show that symbol, the configuration file must have a variable `vcs`
with an option `show_symbol` set to `true` (see
[Segment Configuration](#segment-configuration)).

## Setup

This script uses ANSI color codes to display colors in a terminal. These are
notoriously non-portable, so may not work for you out of the box, but try
setting your $TERM to `xterm-256color`.

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
git clone https://github.com/b-ryan/powerline-shell
cd powerline-shell
python setup.py install
```

- Setup your shell prompt using the instructions for your shell below.

### Bash

Add the following to your `.bashrc` file:

```
function _update_ps1() {
    PS1=$(powerline-shell $?)
}

if [[ $TERM != linux && ! $PROMPT_COMMAND =~ _update_ps1 ]]; then
    PROMPT_COMMAND="_update_ps1; $PROMPT_COMMAND"
fi
```

**Note:** On macOS, you must add this to one of `.bash_profile`, `.bash_login`,
or `.profile`. macOS will execute the files in the aforementioned order and
will stop execution at the first file it finds. For more information on the
order of precedence, see the section **INVOCATION** in `man bash`.

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

if [ "$TERM" != "linux" -a -x "$(command -v powerline-shell)" ]; then
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
expected to be located at `~/.config/powerline-shell/config.json`. You can
generate the default config at this location using:

```
mkdir -p ~/.config/powerline-shell && \
powerline-shell --generate-config > ~/.config/powerline-shell/config.json
```

(As an example, my config file is located here:
[here](https://github.com/b-ryan/dotfiles/blob/master/home/config/powerline-shell/config.json))

### Adding, Removing and Re-arranging segments

Once you have generated your config file, you can now start adding or removing
"segments" - the building blocks of your shell. The list of segments available
can be seen
[here](https://github.com/b-ryan/powerline-shell/tree/master/powerline_shell/segments).

You can also create custom segments. Start by copying an existing segment like
[this](https://github.com/b-ryan/powerline-shell/blob/master/powerline_shell/segments/aws_profile.py).
Make sure to change any relative imports to absolute imports. Ie. change things
like:

```python
from ..utils import BasicSegment
```

to

```python
from powerline_shell.utils import BasicSegment
```

Then change the `add_to_powerline` function to do what you want. You can then
use this segment in your configuration by putting the path to your segment in
the segments section, like:

```json
"segments": [
    "~/path/to/segment.py"
]
```

### Generic Segments

There are two special segments available. `stdout` accepts an arbitrary command
and the output of the command will be put into your prompt. `env` takes an
environment variable and the value of the variable will be set in your prompt.
For example, your config could look like this:

```
{
  "segments": [
    "cwd",
    "git",
    {
      "type": "stdout",
      "command": ["echo", "hi"],
      "fg_color": 22,
      "bg_color": 161
    },
    {
      "type": "env",
      "var": "DOCKER_MACHINE_NAME"
    },
  ]
}
```

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
they miss colors for any segments.

If you want to create a custom theme, start by copying one of the existing
themes, like the
[basic](https://github.com/b-ryan/powerline-shell/blob/master/powerline_shell/themes/basic.py).
and update your `~/.config/powerline-shell/config.json`, setting the `"theme"`
to the path of the file. For example your configuration might have:

```
  "theme": "~/mythemes/my-great-theme.py"
```

You can then modify the color codes to your liking. Theme colors are specified
using [Xterm-256 color codes](https://jonasjacek.github.io/colors/).

A script for testing color combinations is provided at `colortest.py`. Note
that the colors you see may vary depending on your terminal. When designing a
theme, please test your theme on multiple terminals, especially with default
settings.

### Segment Configuration

Some segments support additional configuration. The options for the segment are
nested under the name of the segment itself. For example, all of the options
for the `cwd` segment are set in `~/.config/powerline-shell/config.json` like:

```
{
    "segments": [...],
    "cwd": {
        options go here
    }
    "theme": "theme-name",
    "vcs": {
        options go here
    }
}
```

The options for the `cwd` segment are:

- `mode`: If `plain`, then simple text will be used to show the cwd. If
  `dironly`, only the current directory will be shown. Otherwise expands the
  cwd into individual directories.
- `max_depth`: Maximum number of directories to show in path.
- `max_dir_size`: Maximum number of characters displayed for each directory in
  the path.
- `full_cwd`: If true, the last directory will not be shortened when
  `max_dir_size` is used.

The `hostname` segment provides one option:

- `colorize`: If true, the hostname will be colorized based on a hash of
  itself.

The `vcs` segment provides one option:

- `show_symbol`: If `true`, the version control system segment will start with
  a symbol representing the specific version control system in use in the
  current directory.

The options for the `battery` segment are:

- `always_show_percentage`: If true, show percentage when fully charged on AC.
- `low_threshold`: Threshold percentage for low-battery indicator color.

The options for the `time` segment are:

- `format`: Format string as used by strftime function, e.g. `%H:%M`.

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

See the [FAQ](https://github.com/b-ryan/powerline-shell/wiki/FAQ). If you
continue to have issues, please open an
[issue](https://github.com/b-ryan/powerline-shell/issues/new).
