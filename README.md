# Apache ZooKeeper

[![Build Status]](https://travis-ci.org/sleighzy/ansible-zookeeper)
![Lint Code Base] ![Molecule]

Ansible role for installing and configuring Apache ZooKeeper

This role can be used to install and cluster multiple ZooKeeper nodes, this uses
all hosts defined for the "zookeeper-nodes" group in the inventory file by
default. All servers are added to the zoo.cfg file along with the leader and
election ports.
Firewall ports could be opened after setting true to zookeeper_firewalld variable

## Supported Platforms

- Debian 10.x
- RedHat 7
- RedHat 8
- Ubuntu 18.04.x
- Ubuntu 20.04.x

## Requirements

Java: Java 8 / 11

Ansible 2.9.16 or 2.10.4 are the minimum required versions to workaround an
issue with certain kernels that have broken the `systemd` status check. The
error message "`Service is in unknown state`" will be output when attempting to
start the service via the Ansible role and the task will fail. The service will
start as expected if the `systemctl start` command is run on the physical host.
See <https://github.com/ansible/ansible/issues/71528> for more information.

## Role Variables

| Variable                                 | Default                                                           | Comment                                                        |
|------------------------------------------|-------------------------------------------------------------------|----------------------------------------------------------------|
| zookeeper_mirror                         | <http://www-eu.apache.org/dist/zookeeper>                         ||
| zookeeper_version                        | 3.7.1                                                             ||
| zookeeper_package                        | apache-zookeeper-{{ zookeeper_version }}-bin.tar.gz               ||
| zookeeper_group                          | zookeeper                                                         ||
| zookeeper_user                           | zookeeper                                                         ||
| zookeeper_root_dir                       | /usr/share                                                        ||
| zookeeper_install_dir                    | '{{ zookeeper_root_dir}}/apache-zookeeper-{{zookeeper_version}}'  ||
| zookeeper_dir                            | '{{ zookeeper_root_dir }}/zookeeper'                              ||
| zookeeper_log_dir                        | /var/log/zookeeper                                                ||
| zookeeper_data_dir                       | /var/lib/zookeeper                                                ||
| zookeeper_data_log_dir                   | /var/lib/zookeeper                                                ||
| zookeeper_client_port                    | 2181                                                              ||
| zookeeper_id                             | 1                                                                 | Unique per server and should be declared in the inventory file |
| zookeeper_leader_port                    | 2888                                                              ||
| zookeeper_election_port                  | 3888                                                              ||
| zookeeper_servers                        | zookeeper-nodes                                                   | See below                                                      |
| zookeeper_servers_use_inventory_hostname | false                                                             | See below                                                      |
| zookeeper_environment                    | "JVMFLAGS": "-javaagent:/opt/jolokia/jolokia-jvm-1.6.0-agent.jar" ||
| zookeeper_config_params                  |                                                                   | A key-value dictionary that will be templated into zoo.cfg     |
| zookeeper_firewalld                      | false                                                             ||

## Inventory and zookeeper_servers variable

zookeeper_servers variable above accepts a list of inventory host names.
These will be used in the `zoo.cfg` to configure a multi-server cluster
so the hosts can find each other. By default, the hostname used in
the `zoo.cfg` will be the hostname reported by the `hostname` command on
the server(provided by the ansible_nodename variable). See the example below.

Assuming the below inventory file, and that the `hostname` command returns
only the hostname and does not include the domain name.

```ini
[zookeeper-nodes]
zoo1.foo.com zookeeper_id=1       #hostname command returns "zoo1"
zoo2.foo.com zookeeper_id=2       #hostname command returns "zoo2"
zoo3.foo.com zookeeper_id=3       #hostname command returns "zoo3"
```

And assuming the following role variables:

```yaml
...
    - role: sleighzy.zookeeper
      zookeeper_servers:
        - zoo1.foo.com
        - zoo2.foo.com
        - zoo3.foo.com
```

The templated `zoo.cfg` file will contain the below entries:

```ini
server.1=zoo1:2888:3888
server.2=zoo2:2888:3888
server.3=zoo3:2888:3888
```

If you DO NOT want this behaviour and would like the `zoo.cfg` to template the
inventory_hostname then set `zookeeper_servers_use_inventory_hostname` to `true`

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

## Four Letter Word Commands

ZooKeeper can use commands based on four letter words, see
<https://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_4lw>

The below example uses the stat command to find out which instance is the leader
:

```bash
for i in 1 2 3 ; do
  echo "zookeeper0$i is a "$(echo stat | nc zookeeper0$i 2181 | grep ^Mode | awk '{print $2}');
done
```

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

_Note:_ Due to a breaking change in Molecule 3.1.1 the Docker driver for
Molecule has been removed and the `molecule-driver` module must be installed
separately.

```sh
$ python3 -m venv molecule-venv
$ source molecule-venv/bin/activate
(molecule-venv) $ python3 -m pip install ansible ansible-lint yamllint docker molecule-docker "molecule[docker,lint]"
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

[ansible-lint]: https://docs.ansible.com/ansible-lint/
[ansible molecule]: https://molecule.readthedocs.io/en/latest/
[build status]:
  https://travis-ci.org/sleighzy/ansible-zookeeper.svg?branch=master
[lint code base]:
  https://github.com/sleighzy/ansible-zookeeper/workflows/Lint%20Code%20Base/badge.svg
[mit license]: https://img.shields.io/badge/License-MIT-blue.svg
[molecule]:
  https://github.com/sleighzy/ansible-zookeeper/workflows/Molecule/badge.svg
