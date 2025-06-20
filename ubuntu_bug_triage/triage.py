# This file is part of ubuntu-bug-triage. See LICENSE file for license info.
"""Triage module."""

import itertools
import logging
import os

from launchpadlib.launchpad import Launchpad
from launchpadlib.credentials import UnencryptedFileCredentialStore

from . import BLACKLIST
from .bug import Bug


class Triage:
    """Base triage class."""

    def __init__(self, date, anon):
        """Initialize triage class."""
        self._log = logging.getLogger(__name__)

        self.launchpad = self._launchpad_connect(anon)
        self.date = date

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
            self._log.debug("logging into Launchpad anonymously")
            return Launchpad.login_anonymously(
                "ubuntu-bug-triage", "production", version="devel"
            )

        self._log.debug("logging into Launchpad")
        credential_store = UnencryptedFileCredentialStore(
            os.path.expanduser("~/.lp_creds")
        )
        return Launchpad.login_with(
            "ubuntu-bug-triage",
            "production",
            version="devel",
            credential_store=credential_store,
        )

    @staticmethod
    def _tasks_to_bug_ids(tasks):
        """Take list of tasks and return unique set of bug ids."""
        bugs = []
        for task in tasks:
            bug_id = task.bug_link.split("/")[-1]
            if bug_id not in bugs:
                bugs.append(bug_id)

        return sorted(bugs)


class TeamTriage(Triage):
    """Triage Launchpad bugs for a particular Ubuntu team."""

    def __init__(self, team, date, anon, status, ignore_user, tags, tags_combinator):
        """Initialize Team Triage."""
        super().__init__(date, anon)

        self._log.debug("finding bugs for team: %s", team)
        self.team = self.launchpad.people[team]
        self.status = status
        self.ignore_user = ignore_user
        self.tags = tags
        self.tags_combinator = tags_combinator

    def current_backlog_count(self):
        """Get team's current backlog count."""
        return len(
            self.launchpad.distributions["Ubuntu"].searchTasks(
                bug_subscriber=self.team, status=self.status
            )
        )

    def updated_bugs(self):
        """Print update bugs for a specific date or date range."""
        updated_tasks = self.launchpad.distributions["Ubuntu"].searchTasks(
            modified_since=self.date,
            structural_subscriber=self.team,
            status=self.status,
            tags=self.tags,
            tags_combinator=self.tags_combinator,
        )

        bugs = []
        for bug_id in sorted(self._tasks_to_bug_ids(updated_tasks)):
            bug = Bug(self.launchpad.bugs[bug_id], self.ignore_user)

            if self.team.name in BLACKLIST:
                if self._all_src_on_blacklist(bug.tasks, self.team.name):
                    self._log.debug("skipping bug: %s", bug_id)
                    continue

            if bug.last_active_user not in self.ignore_user:
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

    def __init__(
        self,
        package,
        date,
        anon,
        include_project,
        status,
        ignore_user,
        tags,
        tags_combinator,
    ):
        """Initialize package triage."""
        super().__init__(date, anon)

        self._log.debug("finding bugs for package: %s", package)
        self.package = self.launchpad.distributions["Ubuntu"].getSourcePackage(
            name=package
        )
        self.ignore_user = ignore_user

        if self.package is None and not include_project:
            self._log.warning("warn: no Ubuntu package with that name exists")

        self.project = None
        if include_project:
            try:
                self.project = self.launchpad.projects[package]
            except KeyError:
                self._log.warning("warn: no Launchpad project with that name exists")

        self.task_filters = {
            "status": status,
            "tags": tags,
            "tags_combinator": tags_combinator,
        }

    def current_backlog_count(self):
        """Get packages's current backlog count."""
        count = 0
        if self.package:
            count += len(self.package.searchTasks(**self.task_filters))
        if self.project:
            count += len(self.project.searchTasks(**self.task_filters))
        return count

    def updated_bugs(self):
        """Print update bugs for a specific date or date range."""
        package_tasks = []
        if self.package is not None:
            package_tasks = self.package.searchTasks(
                modified_since=self.date, **self.task_filters
            )
        project_tasks = []
        if self.project is not None:
            project_tasks = self.project.searchTasks(
                modified_since=self.date, **self.task_filters
            )

        # launchpadlib Collections don't support appending one another, so
        # synthesise an iterable containing both the Collections we care about
        updated_tasks = itertools.chain(package_tasks, project_tasks)

        bugs = []
        for bug_id in sorted(self._tasks_to_bug_ids(updated_tasks)):
            bug = Bug(self.launchpad.bugs[bug_id], self.ignore_user)
            if bug.last_active_user not in self.ignore_user:
                bugs.append(bug)

        return bugs
