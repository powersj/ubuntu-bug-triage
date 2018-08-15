# Ubuntu Bug Triage

[![Build Status](https://travis-ci.org/powersj/ubuntu-bug-triage.svg?branch=master)](https://travis-ci.org/powersj/ubuntu-bug-triage) [![Snap Status](https://build.snapcraft.io/badge/powersj/ubuntu-bug-triage.svg)](https://build.snapcraft.io/user/powersj/ubuntu-bug-triage)

## Install

User's can obtain ubuntu-bug-triage from PyPI:

```shell
pip3 install ubuntu-bug-triage
```

A snap is coming soon.

## Usage

Usage is as simple as running the script to get today's bugs needing triage for the 'ubuntu-sever' team. If, however you wish to specify a different team or package that can be added:

```shell
ubuntu-bug-triage [team|package]
ubuntu-bug-triage cloud-init
```

Users can also specify a number of days of bugs to triage:

```shell
ubuntu-bug-triage lxd 10
```

There are also `--json` and `--csv` flags to allow for CSV and JSON output respectively.

Finally, the bugs to triage can be opened automatically in a webbrowser via `--open` flag.
