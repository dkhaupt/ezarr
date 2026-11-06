import pytest

import users_groups_setup
from users_groups_setup import UserGroupSetup


@pytest.fixture
def commands(monkeypatch):
    recorded = []

    def fake_run(args, *args_, **kwargs):
        recorded.append((args, kwargs))

    monkeypatch.setattr(users_groups_setup.subprocess, 'run', fake_run)
    monkeypatch.setattr(users_groups_setup.os, 'getuid', lambda: 1000)
    return recorded


def test_group_created_on_init(commands):
    UserGroupSetup()
    assert (['sudo', 'groupadd', 'mediacenter', '-g', '13000'], {'check': True}) in commands


def test_no_shell_is_used(commands):
    setup = UserGroupSetup(media_dir='/media', config_dir='/config')
    setup.sonarr()
    setup.audiobookshelf()
    for args, kwargs in commands:
        assert isinstance(args, list), args
        assert not kwargs.get('shell', False)


def test_sonarr_exact_commands(commands):
    setup = UserGroupSetup(media_dir='/media', config_dir='/config')
    setup.sonarr()
    expected = [
        ['sudo', 'useradd', 'sonarr', '-u', '13001'],
        ['sudo', 'mkdir', '-pv', '/media/data/media/tv', '-m', '775'],
        ['sudo', 'mkdir', '-pv', '/media/data/usenet/tv', '-m', '775'],
        ['sudo', 'mkdir', '-pv', '/media/data/torrents/tv', '-m', '775'],
        ['sudo', 'chown', '-R', 'sonarr:mediacenter', '/media/data/media/tv'],
        ['sudo', 'chown', '-R', 'sonarr:mediacenter', '/media/data/usenet/tv'],
        ['sudo', 'chown', '-R', 'sonarr:mediacenter', '/media/data/torrents/tv'],
        ['sudo', 'chown', '1000:mediacenter', '/media/data'],
        ['sudo', 'chown', '1000:mediacenter', '/media/data/media'],
        ['sudo', 'chown', '1000:mediacenter', '/media/data/usenet'],
        ['sudo', 'chown', '1000:mediacenter', '/media/data/torrents'],
        ['sudo', 'mkdir', '-p', '/config/sonarr-config'],
        ['sudo', 'chown', '-R', 'sonarr:mediacenter', '/config/sonarr-config'],
        ['sudo', 'chown', '1000:mediacenter', '/config'],
        ['sudo', 'usermod', '-a', '-G', 'mediacenter', 'sonarr'],
    ]
    assert [args for args, _ in commands[1:]] == expected


def test_audiobookshelf_uid_is_13013(commands):
    setup = UserGroupSetup()
    setup.audiobookshelf()
    useradds = [args for args, _ in commands if args[:2] == ['sudo', 'useradd']]
    assert ['sudo', 'useradd', 'audiobookshelf', '-u', '13013'] in useradds


def test_readarr_is_gone():
    assert not hasattr(UserGroupSetup, 'readarr')
