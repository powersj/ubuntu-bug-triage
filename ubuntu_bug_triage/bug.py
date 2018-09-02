# This file is part of ubuntu-bug-triage. See LICENSE file for license info.
"""Bug module."""


class BugTask:
    """Bug Task class."""

    def __init__(self, lp_link):
        """Initialize Bug Task."""
        self._lp = lp_link

        self.src_pkg = self.target.split(' ')[0]

    def __repr__(self):
        """Representation of specific task."""
        return '- %-20s [%s]' % (self.target, self.status)

    @property
    def importance(self):
        """Return importance of bug task."""
        return self._lp.importance

    @property
    def status(self):
        """Return status of bug task."""
        return self._lp.status

    @property
    def target(self):
        """Return target of bug task."""
        return self._lp.bug_target_name


class Bug:
    """Bug class."""

    def __init__(self, lp_link):
        """Initialize bug class."""
        self._lp = lp_link

        self.id = self._lp.id
        self.title = self._lp.title

        self.tasks = []
        for task in self._lp.bug_tasks:
            self.tasks.append(BugTask(task))

    def __eq__(self, other):
        """Two bugs are identical if their ids are equal."""
        return self.id == other.id

    @property
    def affects(self):
        """Create string of all packages affected."""
        return [task.target for task in self.tasks]

    @property
    def url(self):
        """Return URL of bug."""
        return self._lp.web_link

    def to_json(self):
        """Return JSON representation of object."""
        return {
            'id': self.id,
            'title': self.title,
            'affects': self.affects
        }
