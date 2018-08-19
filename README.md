# Ubuntu Bug Triage

[![Build Status](https://travis-ci.org/powersj/ubuntu-bug-triage.svg?branch=master)](https://travis-ci.org/powersj/ubuntu-bug-triage) [![Snap Status](https://build.snapcraft.io/badge/powersj/ubuntu-bug-triage.svg)](https://build.snapcraft.io/user/powersj/ubuntu-bug-triage)

Get involved and help fix Ubuntu bugs! Obtain a list of bugs for an Ubuntu team or package that were created or updated yesterday.

Users can further define the number of days to triage to increase the number of bugs found, the output type to allow machine readable output, or set the behavior to open the bugs in a browser and immediately begin bug triage.

## Install

Users can obtain ubuntu-bug-triage as a snap:

```shell
snap install ubuntu-bug-triage
```

Or via PyPI:

```shell
pip3 install ubuntu-bug-triage
```

## Usage

Usage is as simple as running the script to get today's bugs needing triage for the 'ubuntu-sever' team. If, however you wish to specify a different team or package that can be added:

```shell
ubuntu-bug-triage [team|package]
ubuntu-bug-triage cloud-init
ubuntu-bug-triage foundations-bugs
```

Users can also specify a number of days of bugs to triage:

```shell
ubuntu-bug-triage mysql-5.7 10
```

## Machine Readable Output

There are also `--json` and `--csv` flags to allow for JSON and CSV output respectively. These are available to allow for machine readable output.

## Open in Browser

Users on Ubuntu will be able to click on the Launchpad ID (e.g. 'LP: #1234567') in the output to open the browser. However, if a user wishes to open all the bugs quickly in his or her browser then use the `--open` flag! However, be warned that opening a large number of bugs (i.e. > 15) can lead to multiple browser windows getting opened.
