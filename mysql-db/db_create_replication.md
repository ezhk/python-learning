# Config /etc/mysql/conf.d/master-slave.cnf

    [mysqld_multi]
    mysqld     = /usr/sbin/mysqld
    mysqladmin = /usr/bin/mysqladmin
    user       = root
    
    [mysqld1]
    server-id = 10
    port = 3307
    user = mysql
    
    binlog-do-db = employees
    log-bin = bin1.log
    relay-log = relay1.log
    
    gtid-mode = ON
    enforce-gtid-consistency = ON
    datadir = /var/lib/mysqld-multi/mysqld1
    
    pid-file = mysqld1.pid
    socket = mysqld1.sock
    
    [mysqld2]
    server-id = 99
    port = 3308
    user = mysql
    
    binlog-do-db = employees
    log-bin = bin2.log
    relay-log = relay2.log
    
    gtid-mode = ON
    enforce-gtid-consistency = ON
    datadir = /var/lib/mysqld-multi/mysqld2
    
    pid-file = mysqld2.pid
    socket = mysqld2.sock

# Prepare directories
Disable apparmor:

    $ sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.mysqld
    $ cd /etc/apparmor.d/disable
    $ sudo ln -s /etc/apparmor.d/usr.sbin.mysqld .

Create and init dirs:

    # mkdir -p /var/lib/mysqld-multi/
    # mysqld --initialize-insecure --user=mysql --explicit_defaults_for_timestamp --datadir=/var/lib/mysqld-multi/mysqld1
    # mysqld --initialize-insecure --user=mysql --explicit_defaults_for_timestamp --datadir=/var/lib/mysqld-multi/mysqld2

# Start processes

    # mysqld_multi --defaults-file=/etc/mysql/conf.d/master-slave.cnf start 1
    # mysqld_multi --defaults-file=/etc/mysql/conf.d/master-slave.cnf start 2

# Create DB dump and restore it on master

    # mysqldump --set-gtid-purged=OFF --port=3306 -uroot emptoyees >empl.sql
    # cat empl.sql | mysql -uroot --host=127.0.0.1 --port=3307 -Demployees

# Start replication
When GTID is using, don't need to recover mysql dump on slave.

    # mysql -uroot --host=127.0.0.1 --port=3307 -e"CREATE USER 'repl'@'%' IDENTIFIED BY 'password';"
    # mysql -uroot --host=127.0.0.1 --port=3307 -e"GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';"
    # mysql -uroot --host=127.0.0.1 --port=3308 -e"STOP SLAVE; RESET SLAVE; CHANGE MASTER TO MASTER_HOST='127.0.0.1', MASTER_PORT=3307, MASTER_USER='repl', MASTER_PASSWORD='password', MASTER_AUTO_POSITION=1; START SLAVE;"

# Test mysql replication

    # mysql -uroot --host=127.0.0.1 --port=3307 -Demployees -e"show tables;"
    +---------------------+
    | Tables_in_employees |
    +---------------------+
    | departments         |
    | dept_bonus          |
    | dept_emp            |
    | dept_manager        |
    | employees           |
    | salaries            |
    +---------------------+
    # mysql -uroot --host=127.0.0.1 --port=3308 -Demployees -e"show tables;"
    +---------------------+
    | Tables_in_employees |
    +---------------------+
    | departments         |
    | dept_bonus          |
    | dept_emp            |
    | dept_manager        |
    | employees           |
    | salaries            |
    +---------------------+
    # mysql -uroot --host=127.0.0.1 --port=3307 -Demployees -e"DROP TABLE dept_manager;"
    # mysql -uroot --host=127.0.0.1 --port=3308 -Demployees -e"SHOW TABLES;"
    +---------------------+
    | Tables_in_employees |
    +---------------------+
    | departments         |
    | dept_bonus          |
    | dept_emp            |
    | employees           |
    | salaries            |
    +---------------------+
    
    # mysql -uroot --host=127.0.0.1 --port=3308 -Demployees -e"SHOW SLAVE STATUS\G;"
    *************************** 1. row ***************************
                   Slave_IO_State: Waiting for master to send event
                      Master_Host: 127.0.0.1
                      Master_User: repl
                      Master_Port: 3307
                    Connect_Retry: 60
                  Master_Log_File: bin1.000002
              Read_Master_Log_Pos: 17209693
                   Relay_Log_File: relay2.000005
                    Relay_Log_Pos: 17209896
            Relay_Master_Log_File: bin1.000002
                 Slave_IO_Running: Yes
                Slave_SQL_Running: Yes
                  Replicate_Do_DB:
              Replicate_Ignore_DB:
               Replicate_Do_Table:
           Replicate_Ignore_Table:
          Replicate_Wild_Do_Table:
      Replicate_Wild_Ignore_Table:
                       Last_Errno: 0
                       Last_Error:
                     Skip_Counter: 0
              Exec_Master_Log_Pos: 17209693
                  Relay_Log_Space: 17210176
                  Until_Condition: None
                   Until_Log_File:
                    Until_Log_Pos: 0
               Master_SSL_Allowed: No
               Master_SSL_CA_File:
               Master_SSL_CA_Path:
                  Master_SSL_Cert:
                Master_SSL_Cipher:
                   Master_SSL_Key:
            Seconds_Behind_Master: 0
    Master_SSL_Verify_Server_Cert: No
                    Last_IO_Errno: 0
                    Last_IO_Error:
                   Last_SQL_Errno: 0
                   Last_SQL_Error:
      Replicate_Ignore_Server_Ids:
                 Master_Server_Id: 10
                      Master_UUID: 55223631-508a-11e9-8c06-001c4271c28e
                 Master_Info_File: /var/lib/mysqld-multi/mysqld2/master.info
                        SQL_Delay: 0
              SQL_Remaining_Delay: NULL
          Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
               Master_Retry_Count: 86400
                      Master_Bind:
          Last_IO_Error_Timestamp:
         Last_SQL_Error_Timestamp:
                   Master_SSL_Crl:
               Master_SSL_Crlpath:
               Retrieved_Gtid_Set: 55223631-508a-11e9-8c06-001c4271c28e:1-375
                Executed_Gtid_Set: 55223631-508a-11e9-8c06-001c4271c28e:1-375,
    56f8813e-508a-11e9-8c68-001c4271c28e:1-187
                    Auto_Position: 1
             Replicate_Rewrite_DB:
                     Channel_Name:
               Master_TLS_Version:

It works!
