# This file is part of ubuntu-bug-triage. See LICENSE file for license info.
# flake8: ignore=F811
"""Test triage module."""
import pytest
from mock import Mock

from .triage import Triage


def test_launchpad_login():
    """Test launchpad login."""
    from launchpadlib.credentials import UnencryptedFileCredentialStore

    UnencryptedFileCredentialStore = Mock()  # noqa: F811
    UnencryptedFileCredentialStore.return_value = True

    from launchpadlib.launchpad import Launchpad

    Launchpad.login_with = Mock()
    Launchpad.login_with.return_value = True

    test_triage = Triage(1, False)
    assert test_triage

    with pytest.raises(NotImplementedError):
        test_triage.current_backlog_count()

    with pytest.raises(NotImplementedError):
        test_triage.updated_bugs()


def test_launchpad_login_anon():
    """Test anonymous login."""
    from launchpadlib.credentials import UnencryptedFileCredentialStore

    UnencryptedFileCredentialStore = Mock()  # noqa: F811
    UnencryptedFileCredentialStore.return_value = True

    from launchpadlib.launchpad import Launchpad

    Launchpad.login_anonymously = Mock()
    Launchpad.login_anonymously.return_value = True

    assert Triage(1, True)
