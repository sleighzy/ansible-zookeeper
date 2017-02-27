# ansible-zookeeper

Ansible role for installing and configuring Apache ZooKeeper on RHEL / CentOS 7.

## Requirements

Java: Oracle JDK

Platform: RHEL / CentOS 7

## Role Variables

    zookeeper_version: 3.4.8
    zookeeper_snapshot_dir: /var/lib/zookeeper/data
    zookeeper_client_port: 2181

## Dependencies

No dependencies

## Example Playbook

    - hosts: servers
      roles:
         - { role: sleighzy.zookeeper }

## License

MIT
