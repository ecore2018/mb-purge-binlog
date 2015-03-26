# mb-purge-binlog
Safely Purge MySQL Binary Logs based on oldest replica

Script assumes 3306 default port is used and TCP is the protocol for connectivity.  

## Requirements
- MySQLdb mysql connector for python

## Usage
To use mb-purge-binlog.py you will need a user with SUPER privileges. Currently the script will read a defined config file in ini format. I tested with a local ~/.my.cnf file with user credentials stored as per;

File: ~/.my.cnf
```
[client]
user=purge_user
password=abc123
```

This is subject to change but --user and --password arguments could be implemented.

### No-op/print mode
By ommitting the `--execute` flag no action will be taken. The last line of the output permits you to see the actions that would be taken in execute mode.
```
./mb-purge-binlog -m {master_host} -r {replica_host1},{replica_host2} -c ~/.my.cnf
```

Output
``` 
[moore@localhost ~/scripts/mb-purge-binlog]# ./mb-purge-binlog.py -c ~/.my.cnf -m 192.168.0.25 -r 192.168.0.26
Binary logs from Master: 192.168.0.25
	 mysql-bin.000053
	 mysql-bin.000054
	 mysql-bin.000055
	 mysql-bin.000056
	 mysql-bin.000057
	 mysql-bin.000058
	 mysql-bin.000059
	 mysql-bin.000060
	 mysql-bin.000061
	 mysql-bin.000062
	 mysql-bin.000063
Replica: 192.168.0.26, File: mysql-bin.000063
Logs will be purged to mysql-bin.000063. Supply --execute to perform the purge
```

### Execute mode
Including the `--execute` arguement will perform a destructive action. The output permits you to see the actions that were taken in execute mode.
```
./mb-purge-binlog -m {master_host} -r {replica_host1},{replica_host2} -c ~/.my.cnf --execute
```

Output
``` 
[moore@localhost ~/scripts/mb-purge-binlog]# ./mb-purge-binlog.py -c ~/.my.cnf -m 192.168.0.25 -r 192.168.0.26 --execute
Binlogs purged up to mysql-bin.000063
```

## Todo
Improvements identified at this stage:

  1. Refactor code
  2. Logging
  3. Discover slaves connected to master
  4. username and password arguements 
