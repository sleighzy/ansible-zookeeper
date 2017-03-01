# Apache ZooKeeper

[![Build Status](https://travis-ci.org/sleighzy/ansible-zookeeper.svg?branch=master)](https://travis-ci.org/sleighzy/ansible-zookeeper)

Ansible role for installing and configuring Apache ZooKeeper on RHEL / CentOS 7.

## Requirements

Platform: RHEL / CentOS 7

Java: Oracle JDK

The Oracle Java 8 JDK role from Ansible Galaxy can be used if one is needed.

`$ ansible-galaxy install sleighzy.java-8`

## Role Variables

    zookeeper_version: 3.4.8
    zookeeper_group: zookeeper
    zookeeper_user: zookeeper
    zookeeper_root_dir: /usr/share
    zookeeper_install_dir: '{{ zookeeper_root_dir}}/zookeeper-{{zookeeper_version}}'
    zookeeper_dir: '{{ zookeeper_root_dir }}/zookeeper'
    zookeeper_log_dir: /var/log/zookeeper
    zookeeper_snapshot_dir: /var/lib/zookeeper/data
    zookeeper_client_port: 2181

## Dependencies

No dependencies

## Example Playbook

    - hosts: servers
      roles:
         - sleighzy.zookeeper

## License

MIT
