# Changes

2017-11-25 (version 0.4.3)

* New option for `cwd` segment that allows the last directory to not be
  shortened when `max_dir_size` is used
  ([@jceaser](https://github.com/banga/powerline-shell/pull/321)).

2017-10-16 (version 0.4.2)

* VCS segments will use ASCII `?` instead of a unicode symbol for new files.

2017-10-16 (version 0.4.1)

* Fix cwd bug when `$HOME` ends in a slash
  ([@tbodt](https://github.com/banga/powerline-shell/pull/309))
* Use docker to run tests
  ([@aa8y](https://github.com/banga/powerline-shell/pull/297))

2017-10-06 (version 0.4.0)

* tcsh support

2017-09-30 (version 0.3.1)

* Fix username segment's background color after "su" command
  ([@Fak3](https://github.com/banga/powerline-shell/pull/175))
* New `battery` segment which shows the percentage your battery is charged and
  an icon when your battery is charging.
  ([@wattengard](https://github.com/banga/powerline-shell/pull/204))
* New `aws_profile` segment which shows which AWS profile you are using.
  ([@bryangrimes](https://github.com/banga/powerline-shell/pull/223))

2017-09-30 (version 0.3.0)

* Redo Fossil segment to be consistent with git, svn, etc.
  ([@emansije](https://github.com/banga/powerline-shell/pull/286))
* Fix subshell execution in bash described by
  [pw3nage](https://github.com/njhartwell/pw3nage)
  ([@b-ryan](https://github.com/banga/powerline-shell/pull/282))
* Change SSH segment to just use the text `SSH` instead of showing a lock
  symbol. Closes [#287](https://github.com/banga/powerline-shell/issues/287).

2017-09-18 (version 0.2.2)

* Fix python3 issue in uptime segment. Fixes
  [#291](https://github.com/banga/powerline-shell/issues/291).

2017-09-16 (version 0.2.1)

* Fix issues preventing fish shell from rendering.

2017-09-13 (version 0.2.0)

* Add Bazaar segment
  ([@emansije](https://github.com/banga/powerline-shell/pull/283))
  * And rename properties of RepoStats for clarity
    ([@emansije](https://github.com/banga/powerline-shell/pull/284))
* Rewrite SVN segment to be consistent with git
* Remove duplicate function in colortrans.py
  ([@jmtd](https://github.com/banga/powerline-shell/pull/273))
* Make python 3 check compatible with older Python versions
* New theme! `solarized_light`
  ([@ruturajv](https://github.com/banga/powerline-shell/pull/143)

2017-09-10

* Complete overhaul of the project
  ([@b-ryan](https://github.com/banga/powerline-shell/pull/280))
  * There is now a PyPi package
  * It's significantly faster now
  * Configuration and installation is brand new. See README.md

2017-06-21

* Add `rbenv` segment
  ([@dogo](https://github.com/banga/powerline-shell/pull/260))
* Fix path segment so that current directory is emphasized
  ([@inamiy](https://github.com/banga/powerline-shell/pull/235))

2017-06-20

* Add `newline` segment
  ([@ffried](https://github.com/banga/powerline-shell/pull/266))
* Add `npm_version` segment
  ([@WileESpaghetti](https://github.com/banga/powerline-shell/pull/265))
* Fix issue with conda environments
  ([@drorata](https://github.com/banga/powerline-shell/pull/257))
* Fix jobs segment for Cygwin
  ([@themiwi](https://github.com/banga/powerline-shell/pull/256))

2017-05-15

* Fix the `set_term_title` segment for ZSH
  ([@themiwi](https://github.com/banga/powerline-shell/pull/255))

2016-04-16

* Fix issue around unicode function for python 3

2016-04-01

* Refactor of the way the git segment manages data about git's state.
  ([@b-ryan](https://github.com/milkbikis/powerline-shell/pull/221))

2015-12-26

* Beginnings of unit testing for segments. Included in this change was a
  refactor of the way segments are added to powerline. Now, instead of looking
  for a global `powerline` object, `powerline` is passed into the function to
  add the segment. Segments will also no longer add the segments by calling the
  `add` function themselves.
  ([@b-ryan](https://github.com/milkbikis/powerline-shell/pull/212))
* Python3 fixes for `lib/color_compliment.py`.
  ([@ceholden](https://github.com/milkbikis/powerline-shell/pull/220))

2015-11-25

* `virtual_env` segment now supports environments made with `conda`
  ([@ceholden](https://github.com/milkbikis/powerline-shell/pull/198))

2015-11-21

* Fixes for Python 3 compatibility
  ([@b-ryan](https://github.com/milkbikis/powerline-shell/pull/211))

2015-11-18

* The git segment has gotten a makeover
  ([@MartinWetterwald](https://github.com/milkbikis/powerline-shell/pull/136))
* Fix git segment when git is not on the standard PATH
  ([@andrejgl](https://github.com/milkbikis/powerline-shell/pull/153))
* Fix `--cwd-max-depth` showing duplicates when it's <= 2
  ([@b-ryan](https://github.com/milkbikis/powerline-shell/pull/209))
* Add padding around `exit_code` segment
  ([@phatblat](https://github.com/milkbikis/powerline-shell/pull/205))

2015-10-02

* New option (`--cwd-max-dir-size`) which allows you to limit each directory
  that is displayed to a number of characters. This currently does not apply
  if you are using `--cwd-mode plain`.
  ([@mart-e](https://github.com/milkbikis/powerline-shell/pull/127))

2015-08-26

* New `plain` mode of displaying the current working directory which can be
  used by adding `--cwd-only plain` to `powerline-shell.py`.
  This deprecates the `--cwd-only` option. `--cwd-mode dironly` can be used
  instead. ([@paol](https://github.com/milkbikis/powerline-shell/pull/156))

2015-08-18

* New `time` segment
  ([@filipebarros](https://github.com/milkbikis/powerline-shell/pull/107))

2015-08-01

* Use `print` function for some python3 compatibility
  ([@strycore](https://github.com/milkbikis/powerline-shell/pull/195))

2015-07-31

* The current working directory no longer follows symbolic links
* New `exit_code` segment
  ([@disruptek](https://github.com/milkbikis/powerline-shell/pull/129))

2015-07-30

* Fix ZSH root indicator
  ([@nkcfan](https://github.com/milkbikis/powerline-shell/pull/150))
* Add uptime segment
  ([@marcioAlmada](https://github.com/milkbikis/powerline-shell/pull/139))

2015-07-27

* Use `python2` instead of `python` in hashbangs
  ([@Undeterminant](https://github.com/milkbikis/powerline-shell/pull/100))
* Add `node_version` segment
  ([@mmilleruva](https://github.com/milkbikis/powerline-shell/pull/189))
