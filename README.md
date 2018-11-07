# Apache ZooKeeper

[![Build Status](https://travis-ci.org/sleighzy/ansible-zookeeper.svg?branch=master)](https://travis-ci.org/sleighzy/ansible-zookeeper)

Ansible role for installing and configuring Apache ZooKeeper on RHEL / CentOS 7.

This role can be used to install and cluster multiple ZooKeeper nodes, this uses all hosts defined for the "zookeeper-nodes" group
in the inventory file by default. All servers are added to the zoo.cfg file along with the leader and election ports.

## Requirements

Platform: RHEL / CentOS 7

Java: Java 8

The Oracle Java 8 JDK role from Ansible Galaxy can be used if one is needed.

`$ ansible-galaxy install sleighzy.java-8`

## Role Variables

    zookeeper_version: 3.4.13
    zookeeper_group: zookeeper
    zookeeper_user: zookeeper
    zookeeper_root_dir: /usr/share
    zookeeper_install_dir: '{{ zookeeper_root_dir}}/zookeeper-{{zookeeper_version}}'
    zookeeper_dir: '{{ zookeeper_root_dir }}/zookeeper'
    zookeeper_log_dir: /var/log/zookeeper
    zookeeper_data_dir: /var/lib/zookeeper
    zookeeper_data_log_dir: /var/lib/zookeeper
    zookeeper_client_port: 2181
    zookeeper_id: 1
    zookeeper_leader_port: 2888
    zookeeper_election_port: 3888
    zookeeper_mirror: "http://www-eu.apache.org/dist/zookeeper"
    zookeeper_servers: "{{groups['zookeeper-nodes']}}"
    zookeeper_environment:
        "JVMFLAGS": "-javaagent:/opt/jolokia/jolokia-jvm-1.6.0-agent.jar"


### Default Ports

| Port | Description |
|------|-------------|
| 2181 | Client connection port |
| 2888 | Quorum port for clustering |
| 3888 | Leader election port for clustering |


### Default Directories and Files

 Description                               | Directory / File 
-------------------------------------------|------------------
Installation directory                     | `/usr/share/zookeeper-<version>`
Symlink to install directory               | `/usr/share/zookeeper` 
Symlink to configuration                   | `/etc/zookeeper/zoo.cfg` 
Log files                                  | `/var/log/zookeeper` 
Data directory for snapshots and myid file | `/var/lib/zookeeper` 
Data directory for transaction log files   | `/var/lib/zookeeper` 
Systemd service                            | `/usr/lib/systemd/system/zookeeper.service` 
System Defaults                            | `/etc/default/zookeeper` 

## Starting and Stopping ZooKeeper services
* The ZooKeeper service can be started via: `systemctl start zookeeper`
* The ZooKeeper service can be stopped via: `systemctl stop zookeeper`

## Dependencies

No dependencies

## Example Playbook

    - hosts: servers
      roles:
         - sleighzy.zookeeper

## License

MIT
