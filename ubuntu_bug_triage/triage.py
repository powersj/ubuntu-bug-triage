# This file is part of ubuntu-bug-triage. See LICENSE file for license info.
"""Triage module."""

from datetime import datetime, timedelta
import logging
import os

from launchpadlib.launchpad import Launchpad
from launchpadlib.credentials import UnencryptedFileCredentialStore

from . import BLACKLIST
from .bug import Bug


class Triage:
    """Base triage class."""

    def __init__(self, days, anon):
        """Initialize triage class."""
        self._log = logging.getLogger(__name__)

        self.launchpad = self._launchpad_connect(anon)
        self.ubuntu = self.launchpad.distributions['Ubuntu']
        self.date = (
            datetime.now().date() - timedelta(days=days)
        ).strftime('%Y-%m-%d')

    def current_backlog_count(self):
        """Return the total current backlog count."""
        raise NotImplementedError

    def updated_bugs(self):
        """Return updated bugs."""
        raise NotImplementedError

    def _launchpad_connect(self, anon=False):
        """Use the launchpad module connect to launchpad.

        Will connect you to the Launchpad website the first time you
        run this to authorize your system to connect unless anonymous
        login is specified.
        """
        if anon:
            self._log.debug('logging into Launchpad anonymously')
            return Launchpad.login_anonymously(
                'ubuntu-bug-triage', 'production', version='devel'
            )

        self._log.debug('logging into Launchpad')
        credential_store = UnencryptedFileCredentialStore(
            os.path.expanduser('~/.lp_creds')
        )
        return Launchpad.login_with(
            'ubuntu-bug-triage', 'production', version='devel',
            credential_store=credential_store
        )

    @staticmethod
    def _tasks_to_bug_ids(tasks):
        """Take list of tasks and return unique set of bug ids."""
        bugs = []
        for task in tasks:
            bug_id = task.bug_link.split('/')[-1]
            if bug_id not in bugs:
                bugs.append(bug_id)

        return sorted(bugs)


class TeamTriage(Triage):
    """Triage Launchpad bugs for a particular Ubuntu team."""

    def __init__(self, team, days, anon):
        """Initialize Team Triage."""
        super().__init__(days, anon)

        self._log.debug('finding bugs for team: %s', team)
        self.team = self.launchpad.people[team]

    def current_backlog_count(self):
        """Get team's current backlog count."""
        return len(self.ubuntu.searchTasks(bug_subscriber=self.team))

    def updated_bugs(self):
        """Print update bugs for a specific date or date range."""
        updated_tasks = self.ubuntu.searchTasks(
            modified_since=self.date,
            structural_subscriber=self.team
        )

        bugs = []
        for bug_id in sorted(self._tasks_to_bug_ids(updated_tasks)):
            bug = Bug(self.launchpad.bugs[bug_id])

            if self.team.name in BLACKLIST:
                if self._all_src_on_blacklist(bug.tasks, self.team.name):
                    self._log.debug('skipping bug: %s', bug_id)
                    continue

            bugs.append(bug)

        return bugs

    @staticmethod
    def _all_src_on_blacklist(tasks, team):
        """Test if bug tasks source packages are all on blacklist."""
        for task in tasks:
            if task.src_pkg not in BLACKLIST[team]:
                return False

        return True


class PackageTriage(Triage):
    """Triage Launchpad bugs for a particular package."""

    def __init__(self, package, days, anon):
        """Initialize package triage."""
        super().__init__(days, anon)

        self._log.debug('finding bugs for package: %s', package)
        self.package = self.ubuntu.getSourcePackage(name=package)

    def current_backlog_count(self):
        """Get packages's current backlog count."""
        return len(self.package.searchTasks())

    def updated_bugs(self):
        """Print update bugs for a specific date or date range."""
        updated_tasks = self.package.searchTasks(modified_since=self.date)

        bugs = []
        for bug_id in sorted(self._tasks_to_bug_ids(updated_tasks)):
            bugs.append(Bug(self.launchpad.bugs[bug_id]))

        return bugs
