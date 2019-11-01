# IPVS

- Установить ipvsadm на виртуалку

    ```
    # modprobe ip_vs
    # apt install ipvsadm
    ```

- Установить docker туда же

    ```
    # dpkg -l | grep docker
    ii  docker.io                        18.09.7-0ubuntu1~18.04.4                        arm64        Linux container runtime
    ```

- Поднять несколько контейнеров с веб-сервером по вкусу

    ```
    # mkdir -p /web/srv1
    # mkdir -p /web/srv3
    # echo '<h1>Server 1. Hello, world!</h1>' >/web/srv1/index.html
    # echo '<h1>Server 2. Hello, world!</h1>' >/web/srv2/index.html
    # docker run --name nginx-srv1 -v /web/srv1/:/usr/share/nginx/html:ro -d nginx
    # docker run --name nginx-srv3 -v /web/srv3/:/usr/share/nginx/html:ro -d nginx
    # docker inspect nginx-srv1 | fgrep -i '"ipaddress"' | head -n1
            "IPAddress": "172.17.0.2",
    # docker inspect nginx-srv3 | fgrep -i '"ipaddress"' | head -n1
            "IPAddress": "172.17.0.4",

    // пришлось поправить маршруты, так как моя виртуалка по DHCP получила адрес 172.17.0.3/27
    # ip ro a 172.17.0.2/32 dev docker0
    # ip ro a 172.17.0.4/32 dev docker0

    # curl 172.17.0.2
    <h1>Server 1. Hello, world!</h1>
    # curl 172.17.0.4
    <h1>Server 3. Hello, world!</h1>
    ```

- Создать VIP для балансировки трафика между контейнерами

    ```
    # ipvsadm -A -t 172.17.0.3:80 -s wrr
    # ipvsadm -a -t 172.17.0.3:80 -r 172.17.0.2 -m -w 1
    # ipvsadm -a -t 172.17.0.3:80 -r 172.17.0.4 -m -w 1
    # ipvsadm -ln
        IP Virtual Server version 1.2.1 (size=4096)
        Prot LocalAddress:Port Scheduler Flags
        -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
        TCP  172.17.0.3:80 wrr
        -> 172.17.0.2:80                Masq    1      0          0
        -> 172.17.0.4:80                Masq    1      0          0
    
    // поменяем вес real-server-а
    # ipvsadm -d -t 172.17.0.3:80 -r 172.17.0.4:80
    # ipvsadm -a -t 172.17.0.3:80 -r 172.17.0.4:80 -m -w 2
    # ipvsadm -ln
        IP Virtual Server version 1.2.1 (size=4096)
        Prot LocalAddress:Port Scheduler Flags
        -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
        TCP  172.17.0.3:80 wrr
        -> 172.17.0.2:80                Masq    1      0          0
        -> 172.17.0.4:80                Masq    2      0          0
    ```

- Проверить работоспособность балансировки

    ```
    # curl 172.17.0.3
    <h1>Server 3. Hello, world!</h1>
    # curl 172.17.0.3
    <h1>Server 1. Hello, world!</h1>
    # curl 172.17.0.3
    <h1>Server 3. Hello, world!</h1>
    # curl 172.17.0.3
    <h1>Server 3. Hello, world!</h1>

    // запустим ab и посмотрим на вывод ipvsadm
    # ab -c 20 -n 10000 http://172.17.0.3/
    # sudo ipvsadm -ln
        IP Virtual Server version 1.2.1 (size=4096)
        Prot LocalAddress:Port Scheduler Flags
        -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
        TCP  172.17.0.3:80 wrr
        -> 172.17.0.2:80                Masq    1      4          3044
        -> 172.17.0.4:80                Masq    2      7          6088
    ```

- Чистим за собой

    ```
    # ipvsadm -C
    # ipvsadm -ln
        IP Virtual Server version 1.2.1 (size=4096)
        Prot LocalAddress:Port Scheduler Flags
        -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
    # rmmod ip_vs_wrr ip_vs
    ```
