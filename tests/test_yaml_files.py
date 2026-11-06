import os

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_volumes_example_is_valid_yaml():
    with open(os.path.join(REPO_ROOT, 'volumes-example.yml')) as f:
        doc = yaml.safe_load(f)
    assert 'services' in doc
    assert 'volumes' in doc
    assert doc['services']['sonarr']['image'] == 'lscr.io/linuxserver/sonarr:latest'


def test_docker_compose_is_valid_yaml():
    with open(os.path.join(REPO_ROOT, 'docker-compose.yml')) as f:
        doc = yaml.safe_load(f)
    assert 'services' in doc
    assert 'readarr' not in doc['services']
