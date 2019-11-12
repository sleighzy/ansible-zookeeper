import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('file', [
    ("/usr/share/zookeeper/bin/zkServer.sh")
])
def test_script_exists(host, file):
    file = host.file(file)

    assert file.exists


@pytest.mark.parametrize('file', [
    ("/usr/share/zookeeper/conf/zoo.cfg")
])
def test_config_exists(host, file):
    file = host.file(file)

    assert file.exists


@pytest.mark.parametrize('file, content', [
    ("/etc/zookeeper/zoo.cfg", "server.1=zookeeper-1:2888:3888")
])
def test_zookeeper_server_conf_entry(host, file, content):
    file = host.file(file)

    assert file.contains(content)


@pytest.mark.parametrize('file, content', [
    ("/var/lib/zookeeper/myid", "1")
])
def test_zookeeper_myid_entry(host, file, content):
    file = host.file(file)

    assert file.contains(content)


def test_zookeeper_service_started_enabled(host):
    zookeeper_service = host.service('zookeeper')
    assert zookeeper_service.is_running
    assert zookeeper_service.is_enabled
