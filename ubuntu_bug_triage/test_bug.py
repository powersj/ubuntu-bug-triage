# This file is part of ubuntu-bug-triage. See LICENSE file for license info.
"""Test bug module."""
import random

from .bug import Bug, BugTask


class MockBugTaskRandom:
    """Create a task with random valid options."""

    def __init__(self):
        """Initialize class."""
        self.importance = random.choice(
            ["Wishlist", "Low", "Medium", "High", "Critical", "Undecided"]
        )
        self.status = random.choice(
            [
                "New",
                "Incomplete",
                "Opinion",
                "Invalid",
                "Won't Fix",
                "Confirmed",
                "Triaged",
                "In Progress",
                "Fix Committed",
                "Fix Released",
            ]
        )
        self.bug_target_name = random.choice(["Trusty", "Xenial", "Bionic", "Disco"])


class MockBugTask:
    """Create mock bug task with specific items."""

    def __init__(self):
        """Initialize class."""
        self.importance = "Wishlist"
        self.status = "Triaged"
        self.bug_target_name = "Bionic"


class MockBug:
    """Create fake bug with random tasks."""

    def __init__(self):
        """Initialize class."""
        self.id = "1761240"
        self.title = "SRU pollinate 4.33"
        self.status = "Fix Released"
        self.importance = "Low"
        self.bug_target_name = "pollinate (Ubuntu)"
        self.web_link = (
            "https://bugs.launchpad.net/ubuntu/+source/pollinate/+bug/1761240"
        )
        num_tasks = range(random.randint(1, 8))
        self.bug_tasks = [MockBugTaskRandom() for _ in num_tasks]


class MockBugNoTasks:
    """Create bug with no tasks."""

    def __init__(self):
        """Initialize class."""
        self.id = "1761240"
        self.title = "SRU pollinate 4.33"
        self.status = "Fix Released"
        self.importance = "Low"
        self.bug_target_name = "pollinate (Ubuntu)"
        self.web_link = (
            "https://bugs.launchpad.net/ubuntu/+source/pollinate/+bug/1761240"
        )
        self.bug_tasks = []


class MockBug1234567:
    """Fake bug with specific data."""

    def __init__(self):
        """Initialize class."""
        self.id = "1234567"
        self.title = "Test Bug"
        self.status = "In Progress"
        self.importance = "Critical"
        self.bug_target_name = "cloud-init (Ubuntu)"
        self.web_link = (
            "https://bugs.launchpad.net/ubuntu/+source/cloud-init/+bug/1234567"
        )
        self.bug_tasks = []


class MockBug1111111:
    """Another fake bug with specific data."""

    def __init__(self):
        """Initialize class."""
        self.id = "1111111"
        self.title = "Test Bug 2"
        self.status = "Triaged"
        self.importance = "Wishlist"
        self.bug_target_name = "curtin (Ubuntu)"
        self.web_link = (
            "https://bugs.launchpad.net/ubuntu/+source/cloud-init/+bug/1111111"
        )
        self.bug_tasks = []


def test_bug_class():
    """Test Bug Class."""
    assert Bug(MockBug())


def test_bug_class_no_tasks():
    """Test Bug Class with no tasks."""
    assert Bug(MockBugNoTasks())


def test_bug_same():
    """Verify bug compare works."""
    assert Bug(MockBug1234567()) == Bug(MockBug1234567())


def test_bug_not_same():
    """Verify bug compare works negative case."""
    assert Bug(MockBug1234567()) != Bug(MockBug1111111())


def test_affects():
    """Verify affects is an array."""
    bug = Bug(MockBug())
    assert isinstance(bug.affects, type([]))


def test_no_affects():
    """Verify no affects."""
    bug = Bug(MockBugNoTasks())
    assert isinstance(bug.affects, type([]))
    assert bug.affects == []


def test_url():
    """Verify url is a string."""
    bug = Bug(MockBug())
    assert isinstance(bug.url, str)


def test_json():
    """Verify JSON output."""
    bug = Bug(MockBug1234567())
    json_output = {"id": bug.id, "title": bug.title, "affects": bug.affects}
    assert bug.to_json() == json_output


def test_bug_task():
    """Verify bug task attributes."""
    task = BugTask(MockBugTask())
    assert task.importance == "Wishlist"
    assert task.status == "Triaged"
    assert repr(task) == "- %-20s [%s]" % (task.target, task.status)
