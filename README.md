# Apache ZooKeeper

[![Build Status]](https://travis-ci.org/sleighzy/ansible-zookeeper)
![Lint Code Base] ![Ansible Lint] ![Molecule]

Ansible role for installing and configuring Apache ZooKeeper

This role can be used to install and cluster multiple ZooKeeper nodes, this uses
all hosts defined for the "zookeeper-nodes" group in the inventory file by
default. All servers are added to the zoo.cfg file along with the leader and
election ports.

## Supported Platforms

- Debian 10.x
- RedHat 7
- RedHat 8
- Ubuntu 18.04.x

## Requirements

Java: Java 8 / 11

## Role Variables

| Variable                | Default                                                           |
| ----------------------- | ----------------------------------------------------------------- |
| zookeeper_mirror        | <http://www-eu.apache.org/dist/zookeeper>                         |
| zookeeper_version       | 3.6.2                                                             |
| zookeeper_package       | apache-zookeeper-{{ zookeeper_version }}-bin.tar.gz               |
| zookeeper_group         | zookeeper                                                         |
| zookeeper_user          | zookeeper                                                         |
| zookeeper_root_dir      | /usr/share                                                        |
| zookeeper_install_dir   | '{{ zookeeper_root_dir}}/apache-zookeeper-{{zookeeper_version}}'  |
| zookeeper_dir           | '{{ zookeeper_root_dir }}/zookeeper'                              |
| zookeeper_log_dir       | /var/log/zookeeper                                                |
| zookeeper_data_dir      | /var/lib/zookeeper                                                |
| zookeeper_data_log_dir  | /var/lib/zookeeper                                                |
| zookeeper_client_port   | 2181                                                              |
| zookeeper_id            | 1                                                                 |
| zookeeper_leader_port   | 2888                                                              |
| zookeeper_election_port | 3888                                                              |
| zookeeper_servers       | zookeeper-nodes                                                   |
| zookeeper_environment   | "JVMFLAGS": "-javaagent:/opt/jolokia/jolokia-jvm-1.6.0-agent.jar" |

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

```yaml
- hosts: zookeeper-nodes
  roles:
    - sleighzy.zookeeper
```

## Linting

Linting should be done using [ansible-lint]

```sh
pip3 install ansible-lint --user
```

## Testing

This module uses the [Ansible Molecule] testing framework. This test suite
creates a ZooKeeper cluster consisting of three nodes running within Docker
containers. Each container runs a different OS to test the supported platforms
for this Ansible role.

As per the [Molecule Installation guide] this should be done using a virtual
environment. The commands below will create a Python virtual environment and
install Molecule including the Docker driver.

```sh
$ python3 -m venv molecule-venv
$ source molecule-venv/bin/activate
(molecule-venv) $ python3 -m pip install --user "molecule[docker,lint]"
```

Run playbook and tests. Linting errors need to be corrected before Molecule will
execute any tests. This will run all tests and then destroy the Docker
containers.

```sh
molecule test
```

The below command can be used to run the playbook without the tests. This can be
run multiple times when making changes to the role, and ensuring that operations
are idempotent.

```sh
molecule converge
```

The below commands can be used to just run the tests without tearing everything
down. The command `molecule verify` can be repeated for each test run.

```sh
molecule create
molecule converge
molecule verify
```

Tear down Molecule tests and Docker containers.

```sh
molecule destroy
```

## License

[![MIT license]](https://lbesson.mit-license.org/)

[ansible lint]:
  https://github.com/sleighzy/ansible-zookeeper/workflows/Ansible%20Lint/badge.svg
[ansible-lint]: https://docs.ansible.com/ansible-lint/
[ansible molecule]: https://molecule.readthedocs.io/en/latest/
[build status]:
  https://travis-ci.org/sleighzy/ansible-zookeeper.svg?branch=master
[lint code base]:
  https://github.com/sleighzy/ansible-zookeeper/workflows/Lint%20Code%20Base/badge.svg
[mit license]: https://img.shields.io/badge/License-MIT-blue.svg
[molecule]:
  https://github.com/sleighzy/ansible-zookeeper/workflows/Molecule/badge.svg
