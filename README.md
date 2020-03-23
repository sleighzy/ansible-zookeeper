# Apache ZooKeeper

[![Build Status](https://travis-ci.org/sleighzy/ansible-zookeeper.svg?branch=master)](https://travis-ci.org/sleighzy/ansible-zookeeper)

Ansible role for installing and configuring Apache ZooKeeper on RHEL / CentOS 7.

This role can be used to install and cluster multiple ZooKeeper nodes, this uses
all hosts defined for the "zookeeper-nodes" group in the inventory file by
default. All servers are added to the zoo.cfg file along with the leader and
election ports.

## Requirements

Platform: RHEL / CentOS 7

Java: Java 8

## Role Variables

    zookeeper_mirror: http://www-eu.apache.org/dist/zookeeper
    zookeeper_version: 3.6.0
    zookeeper_package: apache-zookeeper-{{ zookeeper_version }}-bin.tar.gz
    zookeeper_group: zookeeper
    zookeeper_user: zookeeper
    zookeeper_root_dir: /usr/share
    zookeeper_install_dir: '{{ zookeeper_root_dir}}/apache-zookeeper-{{zookeeper_version}}'
    zookeeper_dir: '{{ zookeeper_root_dir }}/zookeeper'
    zookeeper_log_dir: /var/log/zookeeper
    zookeeper_data_dir: /var/lib/zookeeper
    zookeeper_data_log_dir: /var/lib/zookeeper
    zookeeper_client_port: 2181
    zookeeper_id: 1
    zookeeper_leader_port: 2888
    zookeeper_election_port: 3888
    zookeeper_servers: "{{groups['zookeeper-nodes']}}"
    zookeeper_environment:
        "JVMFLAGS": "-javaagent:/opt/jolokia/jolokia-jvm-1.6.0-agent.jar"

### Default Ports

| Port | Description                         |
| ---- | ----------------------------------- |
| 2181 | Client connection port              |
| 2888 | Quorum port for clustering          |
| 3888 | Leader election port for clustering |

### Default Directories and Files

| Description                                | Directory / File                            |
| ------------------------------------------ | ------------------------------------------- |
| Installation directory                     | `/usr/share/apache-zookeeper-<version>`     |
| Symlink to install directory               | `/usr/share/zookeeper`                      |
| Symlink to configuration                   | `/etc/zookeeper/zoo.cfg`                    |
| Log files                                  | `/var/log/zookeeper`                        |
| Data directory for snapshots and myid file | `/var/lib/zookeeper`                        |
| Data directory for transaction log files   | `/var/lib/zookeeper`                        |
| Systemd service                            | `/usr/lib/systemd/system/zookeeper.service` |
| System Defaults                            | `/etc/default/zookeeper`                    |

## Starting and Stopping ZooKeeper services

- The ZooKeeper service can be started via: `systemctl start zookeeper`
- The ZooKeeper service can be stopped via: `systemctl stop zookeeper`

## Dependencies

No dependencies

## Example Playbook

    - hosts: zookeeper-nodes
      roles:
         - sleighzy.zookeeper

## Linting

Linting should be done using
[ansible-lint](https://docs.ansible.com/ansible-lint/)

    pip3 install ansible-lint --user

## Testing

This module uses [Molecule](https://molecule.readthedocs.io/en/stable/) as a
testing framework.

As per the
[Molecule Installation guide](https://molecule.readthedocs.io/en/stable/installation.html)
this should be done using a virtual environment. The commands below will create
a Python virtual environment and install Molecule including the Docker driver.

    virtualenv . && \
        source ./bin/activate && \
        pip install 'molecule[docker]' && \
        molecule create

Run playbook and tests. Linting errors need to be corrected before Molecule will
execute any tests.

    molecule test

The below command can be used to run the playbook without the tests. This can be
run multiple times when making changes to the role, and ensuring that operations
are idempotent.

    molecule converge

Tear down Molecule tests and Docker container.

    molecule destroy

## License

MIT
