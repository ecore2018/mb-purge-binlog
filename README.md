# mb-purge-binlog
Safely Purge MySQL Binary Logs based on oldest replica

## Requirements
- MySQLdb mysql connector for python

## Usage
To use mb-purge-binlog.py you will need a user with SUPER privileges. Currently the script will read a defined config file in ini format. I tested with a local ~/.my.cnf file with user credentials stored as per;

File: ~/.my.cnf
```[client]
user=purge_user
password=abc123
```
This is subject to change but --user and --password arguments could be implemented.

### No-op mode

``` ./mb-purge-binlog -m {master_host} -r {replica_host1},{replica_host2} -c ~/.my.cnf
```

### Exec More
