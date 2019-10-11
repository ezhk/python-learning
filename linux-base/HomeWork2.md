- Выяснить, для чего предназначена команда cat. Используя данную команду, создайте два файла с данными, а затем объедините их в один. Просмотрите содержимое созданного файла. Переименуйте файл, дав ему новое имя.

    ```
    $ cat /etc/protocols /etc/services >one_file
    $ mv one_file another_file
    $ rm another_file
    ```

- Создать несколько файлов. Создайте директорию, переместите файл туда. Удалите все созданные в этом и предыдущем задании директории и файлы.

    См. предпоследнее задание с созданием файлов по месяца, датам и пр.

- В ОС Linux скрытыми файлами считаются те, имена которых начинаются с символа “.”. Сколько скрытых файлов в вашем домашнем каталоге? (Использовать конвейер. Подсказка: для подсчета количества строк можно использовать wc).

    ```
    $ find ~ -name ".*" -type f | wc -l
    10
    ```

- Попробовать вывести с помощью cat все файлы в директории /etc. Направить ошибки в отдельный файл в вашей домашней директории. Сколько файлов, которые не удалось посмотреть, оказалось в списке?

    ```
    $ find /etc/ -type f -exec cat {} \; 2>errors 1>/dev/null

    $ tail errors
    cat: /etc/ufw/before6.rules: Permission denied
    cat: /etc/ufw/before.init: Permission denied
    cat: /etc/ufw/user6.rules: Permission denied
    cat: /etc/ufw/after.rules: Permission denied
    cat: /etc/ufw/after.init: Permission denied
    cat: /etc/sudoers.d/README: Permission denied
    cat: /etc/sudoers: Permission denied
    cat: /etc/.pwd.lock: Permission denied
    cat: /etc/gshadow: Permission denied
    cat: /etc/passwd-: Permission denied

    $ wc -l errors
    35 errors
    ```

- Запустить в одном терминале программу, в другом терминале посмотреть PID процесса и остановить с помощью kill, посылая разные типы сигналов. Что происходит?

    ```
    $ sleep 120
    Killed
    ```

- *Отобразить в /dev список устройств, которые в настоящее время используются вашим UID (для этого используется команда lsof). Организовать конвейер через less, чтобы посмотреть их должным образом.

    ```
    # id -u | xargs lsof +f -u | grep "/dev/" | head
    systemd       1 root    0u      CHR                1,3      0t0          6 /dev/null
    systemd       1 root    1u      CHR                1,3      0t0          6 /dev/null
    systemd       1 root    2u      CHR                1,3      0t0          6 /dev/null
    systemd       1 root   18r      CHR             10,235      0t0        395 /dev/autofs
    systemd       1 root   86u      CHR              10,62      0t0          4 /dev/rfkill
    systemd-j   418 root    0r      CHR                1,3      0t0          6 /dev/null
    systemd-j   418 root    1w      CHR                1,3      0t0          6 /dev/null
    systemd-j   418 root    2w      CHR                1,3      0t0          6 /dev/null
    systemd-j   418 root    7w      CHR               1,11      0t0         12 /dev/kmsg
    systemd-j   418 root    9u      CHR               1,11      0t0         12 /dev/kmsg
    ```

- *Cоздайте директорию для хранения фотографий, в ней должны быть директории по годам, (например, за последние 5 лет), и в каждой директории года по директории для месяца.
*Заполните директории файлами вида ГГГГММДДНН.txt. Внутри файла должно быть имя файла. Например 2018011301.txt, 2018011302.txt.

    ```
    $ ./dirs.sh
    $ cat dirs.sh
        startFilename="2019/01/01/00.txt"
        endFilename="2019/10/12/00.txt"

        daysShift=0
        currentDate=endFilename
        while :
        do
            currentFilename=$(date "+%Y/%m/%d/%H.txt" --date "${daysShift} hour")
            test "${currentFilename}" == "${startFilename}" && break

            mkdir -p $(dirname ${currentFilename})
            touch ${currentFilename}
            daysShift=$((${daysShift} - 1))
        done
    $ find 2019 -type f | head
        2019/04/16/21.txt
        2019/04/16/03.txt
        2019/04/16/07.txt
        2019/04/16/20.txt
        2019/04/16/14.txt
        2019/04/16/08.txt
        2019/04/16/12.txt
        2019/04/16/04.txt
        2019/04/16/05.txt
        2019/04/16/09.txt
    $ rm -rf 2019/
    ```

10. * Полезное задание на конвейер. Использовать команду cut на вывод длинного списка каталога, чтобы отобразить только права доступа к файлам. Затем отправить в конвейере этот вывод на sort и uniq, чтобы отфильтровать все повторяющиеся строки. Потом с помощью wc посчитать различные типы разрешений в этом каталоге. Самостоятельно решить задачу, как сделать так, чтобы в подсчет не добавлялись строка Итого и файлы . и .. (ссылки на текущую и родительскую директории)

    ```
    # ls -l /etc | cut -d ' ' -f 1 | grep "^-" | sort | uniq
    -r--r-----
    -r--r--r--
    -rw-------
    -rw-r-----
    -rw-r--r--
    -rwxr-xr-x
    ```
