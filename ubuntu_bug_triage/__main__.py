# This file is part of ubuntu-bug-triage. See LICENSE file for license info.
"""Ubuntu Bug Triage module."""

import argparse
from datetime import datetime, timedelta
import logging
import sys

from . import UBUNTU_PACKAGE_TEAMS
from . import ACTIONABLE_BUG_STATUSES
from .triage import PackageTriage, TeamTriage
from .view import BrowserView, CSVView, JSONView, TerminalView


def parse_args():
    """Set up command-line arguments."""
    parser = argparse.ArgumentParser("ubuntu-bug-triage")
    parser.add_argument(
        "package_or_team",
        nargs="?",
        default="ubuntu-server",
        help="""source package name (e.g. cloud-init, lxd) or package team name
        (e.g. ubuntu-openstack, foundations-bugs) to use for search (default:
        ubuntu-server)""",
    )
    parser.add_argument(
        "days",
        nargs="?",
        type=int,
        default=1,
        help="""number of days (e.g 1, 10) of bugs to triage, where one day is
        the default. Use --start-time to use a specific date.""",
    )
    parser.add_argument(
        "--anon", action="store_true", help="Anonymous login to Launchpad"
    )
    parser.add_argument("--csv", action="store_true", help="output as CSV")
    parser.add_argument(
        "--debug", action="store_true", help="additional logging output"
    )
    parser.add_argument(
        "--ignore-user",
        default=[],
        nargs="*",
        help="""ignore bugs edited last by the listed person""",
    )
    parser.add_argument("--json", action="store_true", help="output as JSON")
    parser.add_argument(
        "--open", action="store_true", help="open resulting bugs in web browser"
    )
    parser.add_argument(
        "--include-project",
        "-p",
        action="store_true",
        help="include project bugs in output",
    )
    parser.add_argument(
        "--start-time",
        help="""a date and time (e.g. '2020-10-01 14:15') to start triage
        from. This will override the value set by days.""",
    )
    parser.add_argument(
        "--status",
        "-s",
        action="append",
        default=[],
        metavar="STATUS",
        choices=[
            "any",
            "New",
            "Incomplete",
            "Opinion",
            "Invalid",
            "Won't Fix",
            "Expired",
            "Confirmed",
            "Triaged",
            "In Progress",
            "Fix Committed",
            "Fix Released",
            "Incomplete (with response)",
            "Incomplete (without response)",
        ],
        help="Restrict the search to bugs with the given status."
        " Can be specified multiple times. Defaults: "
        + ", ".join(ACTIONABLE_BUG_STATUSES)
        + ".",
    )
    parser.add_argument(
        "--urls", action="store_true", help="print only the urls of bugs to triage"
    )

    return parser.parse_args()


def parse_date(args):
    """Parse either the number of days for triage or specific date time."""
    if args.start_time:
        try:
            date = datetime.strptime(args.start_time, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Oops: invalid format or date for start time. Use '%Y-%m-%d %H:%M'")
            sys.exit(1)
    else:
        date = datetime.now() - timedelta(days=args.days)

    return date.strftime("%Y-%m-%dT%H:%M")


def setup_logging(debug):
    """Set up logging."""
    logging.basicConfig(
        stream=sys.stdout,
        format="%(message)s",
        level=logging.DEBUG if debug else logging.INFO,
    )


def launch():
    """Launch ubuntu-bug-triage."""
    args = parse_args()
    if not args.status:
        args.status = ACTIONABLE_BUG_STATUSES
    elif "any" in args.status:
        args.status = []
    args.status = list(set(args.status))
    setup_logging(args.debug)
    date = parse_date(args)

    if args.package_or_team in UBUNTU_PACKAGE_TEAMS:
        if args.include_project:
            logging.getLogger(__name__).warning(
                "N.B. --include-project has no effect when running against a"
                " package team"
            )
        triage = TeamTriage(
            args.package_or_team, date, args.anon, args.status, args.ignore_user
        )
    else:
        triage = PackageTriage(
            args.package_or_team,
            date,
            args.anon,
            args.include_project,
            args.status,
            args.ignore_user,
        )

    bugs = triage.updated_bugs()
    if args.urls:
        for bug in bugs:
            print(bug.url)
    elif args.csv:
        CSVView(bugs)
    elif args.json:
        JSONView(bugs)
    else:
        TerminalView(bugs)

    if args.open:
        BrowserView(bugs)


if __name__ == "__main__":
    sys.exit(launch())
