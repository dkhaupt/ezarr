import re

import yaml

from container_configs import ContainerConfig

GLUETUN_BLOCK = (
    '  gluetun:\n'
    '    image: qmcgaw/gluetun@sha256:89e3cbe22e0d6f09a18d3e86269392fd9f7f08e8991040741e577f8f127cdfe4\n'
    '    container_name: gluetun\n'
    '    cap_add:\n'
    '      - NET_ADMIN\n'
    '    environment:\n'
    '      - VPN_SERVICE_PROVIDER=mullvad\n'
    '      - VPN_TYPE=wireguard\n'
    '      - WIREGUARD_PRIVATE_KEY=${WIREGUARD_PRIVATE_KEY}\n'
    '      - WIREGUARD_ADDRESSES=${WIREGUARD_ADDRESSES}\n'
    '      - SERVER_CITIES=Stockholm,Amsterdam\n'
    '    ports:\n'
    '      - "8080:8080" # qbittorrent\n'
    '      - "6881:6881" # qbittorrent\n'
    '      - "6881:6881/udp" # qbittorrent\n'
    '      - "8484:8484" # sabnzbd\n'
    '    devices:\n'
    '      - "/dev/net/tun:/dev/net/tun"\n'
    '    restart: unless-stopped\n\n'
)

ALL_SERVICES = [
    'sonarr',
    'radarr',
    'lidarr',
    'mylar3',
    'audiobookshelf',
    'prowlarr',
    'qbittorrent',
    'overseerr',
    'plex',
    'tautulli',
    'jellyfin',
    'jellyseerr',
    'sabnzbd',
]


def build_compose():
    config = ContainerConfig(
        media_dir='/media',
        config_dir='/config',
        timezone='Europe/Amsterdam',
        plex_claim='test-claim',
    )
    text = '---\nservices:\n' + GLUETUN_BLOCK
    for service in ALL_SERVICES:
        text += getattr(config, service)()
    return text


def parse_port(entry):
    entry = entry.strip().strip('"')
    host, _, container = entry.partition(':')
    protocol = 'tcp'
    if '/' in container:
        container, protocol = container.rsplit('/', 1)
    return host, protocol


def test_generated_compose_is_valid_yaml():
    doc = yaml.safe_load(build_compose())
    assert 'services' in doc
    assert set(doc['services'].keys()) == {'gluetun'} | set(ALL_SERVICES)


def test_puid_pugid_uniqueness():
    doc = yaml.safe_load(build_compose())
    literal = []
    for name, service in doc['services'].items():
        for env in service.get('environment', []):
            key, _, value = env.partition('=')
            if key == 'PUID' and value.isdigit():
                literal.append((name, value))
    values = [value for _, value in literal]
    assert len(values) == len(set(values)), 'duplicate PUIDs: ' + str(literal)


def test_pgid_consistent():
    doc = yaml.safe_load(build_compose())
    for name, service in doc['services'].items():
        for env in service.get('environment', []):
            key, _, value = env.partition('=')
            if key == 'PGID':
                assert value == '13000', (name, env)


def test_host_ports_unique():
    doc = yaml.safe_load(build_compose())
    seen = []
    for name, service in doc['services'].items():
        for port in service.get('ports', []):
            host, protocol = parse_port(port)
            seen.append((name, host, protocol))
    pairs = [(host, protocol) for _, host, protocol in seen]
    assert len(pairs) == len(set(pairs)), 'duplicate host ports: ' + str(seen)


def test_network_mode_format():
    doc = yaml.safe_load(build_compose())
    for name, service in doc['services'].items():
        mode = service.get('network_mode')
        if mode is None:
            continue
        assert mode == 'host' or re.fullmatch(r'service:[a-z0-9_-]+', mode), (name, mode)
        if mode.startswith('service:'):
            assert 'ports' not in service, name + ' may not combine ports with a service network mode'
            target = mode.split(':', 1)[1]
            assert target in doc['services'], 'unknown network target for ' + name
