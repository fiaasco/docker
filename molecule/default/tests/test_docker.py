import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('pkg', ['docker-ce', 'containerd.io', 'docker-ce-cli', 'python-docker'])
def test_docker_packages(host, pkg):
    assert host.package(pkg).is_installed


def test_docker_compose(host):
    compose = host.file('/usr/local/bin/docker-compose')
    assert compose.exists
    assert compose.user == 'root'
    assert compose.group == 'docker'


def test_docker_compose_exec(host):
    command = host.run("/usr/local/bin/docker-compose version")
    assert command.rc == 0
    assert "docker-compose" in command.stdout
    assert "docker-py" in command.stdout


def test_docker_hello_world(host):
    command = host.run("docker run hello-world")
    assert "This message shows that your installation appears to be working correctly." in command.stdout


def test_docker_service(host):
    assert host.service('docker').is_enabled
    assert host.service('docker').is_running
