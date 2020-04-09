# This file is part of ubuntu-bug-triage. See LICENSE file for license info.
# pylint: disable=redefined-outer-name, no-member
"""Test view module."""
from mock import Mock
import pytest

from .bug import Bug
from .test_bug import MockBug1234567
from .view import TerminalView, CSVView, JSONView, BrowserView


@pytest.fixture(scope="module")
def bugs():
    """Create array of bugs for testing."""
    return [Bug(MockBug1234567()), Bug(MockBug1234567())]


def test_browser_view(bugs):
    """Test out browser is launched."""
    # mock out the sleeps to prevent slowing down unit tests
    import time

    time.sleep = Mock()
    time.sleep.return_value = None

    # mock out webbrowser open and open tab functions
    import webbrowser

    webbrowser.open = Mock()
    webbrowser.open.return_value = True
    webbrowser.open_new_tab = Mock()
    webbrowser.open_new_tab.return_value = True

    assert BrowserView(bugs)
    assert webbrowser.open.called
    assert webbrowser.open_new_tab.called


def test_csv_view(bugs):
    """Test CSV view."""
    assert CSVView(bugs)


def test_json_view(bugs):
    """Test JSON view."""
    assert JSONView(bugs)


def test_terminal_view(bugs):
    """Test terminal view."""
    # Mock out the terminal width call
    import os

    os.popen = Mock()
    os.popen.return_value.read.return_value.split.return_value = "80"

    assert TerminalView(bugs)
