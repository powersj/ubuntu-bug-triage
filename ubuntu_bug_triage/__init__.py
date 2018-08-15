# This file is part of ubuntu-bug-triage. See LICENSE file for license info.
"""Ubuntu Bug Triage module."""

# This is a hard-coded list of teams that produce a lot of bugs and may
# not want to be included in the full team triage.
#
BLACKLIST = {
    'ubuntu-server': [
        'cloud-init',
        'curtin',
        'juju',
        'juju-core',
        'lxc',
        'lxd',
        'maas'
    ]
}

# This is hard-coded as it took way too long to download the json file
# from the following URL:
#
# https://people.canonical.com/~ubuntu-archive/package-team-mapping.json
#
UBUNTU_PACKAGE_TEAMS = [
    'pkg-ime',
    'ubuntu-openstack',
    'documentation-packages',
    'kubuntu-bugs',
    'checkbox-bugs',
    'foundations-bugs',
    'maas-maintainers',
    'ubuntu-server',
    'ubuntu-printing',
    'ubuntu-security-bugs',
    'mir-team',
    'kernel-packages',
    'unsubscribed',
    'desktop-packages',
    'translators-packages',
    'snappy-dev',
]
