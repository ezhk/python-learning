- Создать файл file1 и наполнить его произвольным содержимым. Скопировать его в file2. Создать символическую ссылку file3 на file1. Создать жесткую ссылку file4 на file1. Посмотреть, какие айноды у файлов. Удалить file1. Что стало с остальными созданными файлами? Попробовать вывести их на экран.

    ```
    8baf87a55af1# apt install openssl
    8baf87a55af1# openssl rand -out file1 -base64 128
    8baf87a55af1# cat file1
    6EF6X5SKwwRpTB0IxSHtg6VikSG3HagZisVkSvYtXSwyLj046NTpv54on40VMJkv
    Nam+UkURBDxBToTlQ9o2RalgAjJfFC2WV2zCip6COKbs49qx+AegwhEVVsL1OjX4
    u6ct9aLv2I1j/+zaKICriZK3qKAY5d7rPC+hiSqc6d8=

    8baf87a55af1# cp file1 file2
    8baf87a55af1# ln -sf file1 file3

    8baf87a55af1# ln file1 file4
    8baf87a55af1# ls -lai file?
    1180554 -rw-r--r-- 2 root root 175 Oct 15 09:07 file1
    1180559 -rw-r--r-- 1 root root 175 Oct 15 09:08 file2
    1180580 lrwxrwxrwx 1 root root   5 Oct 15 09:08 file3 -> file1
    1180554 -rw-r--r-- 2 root root 175 Oct 15 09:07 file4

    8baf87a55af1# rm file1
    8baf87a55af1# ls -lai file?
    1180559 -rw-r--r-- 1 root root 175 Oct 15 09:08 file2
    1180580 lrwxrwxrwx 1 root root   5 Oct 15 09:08 file3 -> file1
    1180554 -rw-r--r-- 1 root root 175 Oct 15 09:07 file4
    8baf87a55af1# cat file3
    cat: file3: No such file or directory
    8baf87a55af1# cat file4
    6EF6X5SKwwRpTB0IxSHtg6VikSG3HagZisVkSvYtXSwyLj046NTpv54on40VMJkv
    Nam+UkURBDxBToTlQ9o2RalgAjJfFC2WV2zCip6COKbs49qx+AegwhEVVsL1OjX4
    u6ct9aLv2I1j/+zaKICriZK3qKAY5d7rPC+hiSqc6d8=
    ```

- Дать созданным файлам другие, произвольные имена. Создать новую символическую ссылку. Переместить ссылки в другую директорию.

    ```
    8baf87a55af1# mv secondfile file_second
    8baf87a55af1# ls -li file_*
    1180606 -rw-r--r-- 1 root root 175 Oct 15 09:11 file_rand
    1180559 -rw-r--r-- 1 root root 175 Oct 15 09:08 file_second

    8baf87a55af1# ln -sf file_rand test_link
    8baf87a55af1# ln file_second test_hardlink
    8baf87a55af1# ls -la file_* test_*
    -rw-r--r-- 1 root root 175 Oct 15 09:13 file_rand
    -rw-r--r-- 2 root root 175 Oct 15 09:08 file_second
    -rw-r--r-- 2 root root 175 Oct 15 09:08 test_hardlink
    lrwxrwxrwx 1 root root   9 Oct 15 09:13 test_link -> file_rand

    8baf87a55af1# mkdir testdir
    8baf87a55af1# mv test_link testdir
    8baf87a55af1# mv test_hardlink testdir
    8baf87a55af1# ls -lai testdir/
    total 12
    43216 drwxr-xr-x 2 root root 4096 Oct 15 09:14 .
    39281 drwxr-xr-x 1 root root 4096 Oct 15 09:14 ..
    1180559 -rw-r--r-- 2 root root  175 Oct 15 09:08 test_hardlink
    1180580 lrwxrwxrwx 1 root root    9 Oct 15 09:13 test_link -> file_rand # в этой директории этого файла нет, путь относительный

    8baf87a55af1# cat testdir/test_link
    cat: testdir/test_link: No such file or directory
    8baf87a55af1# cat testdir/test_hardlink
    6EF6X5SKwwRpTB0IxSHtg6VikSG3HagZisVkSvYtXSwyLj046NTpv54on40VMJkv
    Nam+UkURBDxBToTlQ9o2RalgAjJfFC2WV2zCip6COKbs49qx+AegwhEVVsL1OjX4
    u6ct9aLv2I1j/+zaKICriZK3qKAY5d7rPC+hiSqc6d8=
    ```

- Создать два произвольных файла. Первому присвоить права на чтение, запись для владельца и группы, только на чтение для всех. Второму присвоить права на чтение, запись только для владельца. Сделать это в численном и символьном виде.

    ```
    8baf87a55af1# touch first second
    8baf87a55af1# ls -la first second
    -rw-r--r-- 1 root root 0 Oct 15 08:56 first
    -rw-r--r-- 1 root root 0 Oct 15 08:56 second
    8baf87a55af1# chmod 664 first
    8baf87a55af1# chmod 600 second
    8baf87a55af1# ls -la first second
    -rw-rw-r-- 1 root root 0 Oct 15 08:56 first
    -rw------- 1 root root 0 Oct 15 08:56 second

    8baf87a55af1# chmod 000 first second
    8baf87a55af1# ls -la first second
    ---------- 1 root root 0 Oct 15 08:56 first
    ---------- 1 root root 0 Oct 15 08:56 second
    8baf87a55af1# chmod a+r first ; chmod ug+w first ; chmod u+rw second
    8baf87a55af1# ls -la first second
    -rw-rw-r-- 1 root root 0 Oct 15 08:56 first
    -rw------- 1 root root 0 Oct 15 08:56 second
    ```

- Создать пользователя, обладающего возможностью выполнять действия от имени суперпользователя.

    ```
    8baf87a55af1# groupadd test
    8baf87a55af1# useradd -d /home/test -s /bin/bash -g test -m -r test

    8baf87a55af1# apt install sudo
    8baf87a55af1# usermod -g test -G sudo test

    8baf87a55af1# passwd test
    Enter new UNIX password:
    Retype new UNIX password:
    passwd: password updated successfully
    8baf87a55af1# su - test

    test@8baf87a55af1:~$ sudo uptime
    [sudo] password for test:
    09:02:38 up 1 day,  9:19,  0 users,  load average: 0.00, 0.00, 0.00
    test@8baf87a55af1:~$ id
    uid=999(test) gid=1000(test) groups=1000(test),27(sudo)
    test@8baf87a55af1:~$ sudo id
    uid=0(root) gid=0(root) groups=0(root)
    ```

- Создать группу developer, несколько пользователей, входящих в эту группу. Создать директорию для совместной работы. Сделать так, чтобы созданные одними пользователями файлы могли изменять другие пользователи этой группы.

    ```
    8baf87a55af1# groupadd developer
    8baf87a55af1# useradd -G developer -s /bin/bash dev-one
    8baf87a55af1# useradd -G developer -s /bin/bash dev-two
    8baf87a55af1# useradd -G developer -s /bin/bash dev-three
    8baf87a55af1#
    8baf87a55af1# mkdir /var/tmp/exchange
    8baf87a55af1# chown :developer /var/tmp/exchange

    Ставим директории SGID флаг.

    8baf87a55af1# chmod 2775 /var/tmp/exchange
    8baf87a55af1# ls -al /var/tmp/|grep exch
    drwxrwsr-x 2 root developer 4096 Oct 15 09:16 exchange
    8baf87a55af1# su - dev-one
    No directory, logging in with HOME=/
    dev-one@8baf87a55af1:/$ touch /var/tmp/exchange/my_file_1
    dev-one@8baf87a55af1:/$ logout
    8baf87a55af1# ls -al /var/tmp/exchange/my_file_1
    -rw-rw-r-- 1 dev-one developer 0 Oct 15 09:18 /var/tmp/exchange/my_file_1
    ```

- Создать в директории для совместной работы поддиректорию для обмена файлами, но чтобы удалять файлы могли только их создатели.

    ```
    8baf87a55af1# mkdir /var/tmp/newdir
    8baf87a55af1# chown :developer /var/tmp/newdir

    Для директории ставим SGID флаг и sticky.

    8baf87a55af1# chmod 3775 /var/tmp/newdir
    8baf87a55af1# ls -al /var/tmp|grep newdir
    drwxrwsr-t 2 root developer 4096 Oct 15 09:21 newdir
    8baf87a55af1# su - dev-one
    No directory, logging in with HOME=/
    dev-one@8baf87a55af1:/$ echo "text" > /var/tmp/newdir/newfile
    dev-one@8baf87a55af1:/$ logout
    8baf87a55af1# su - dev-two
    No directory, logging in with HOME=/
    dev-two@8baf87a55af1:/$ cat /var/tmp/newdir/newfile
    text
    dev-two@8baf87a55af1:/$ ls -la /var/tmp/newdir/newfile
    -rw-rw-r-- 1 dev-one developer 5 Oct 15 09:22 /var/tmp/newdir/newfile
    dev-two@8baf87a55af1:/$ rm /var/tmp/newdir/newfile
    rm: cannot remove '/var/tmp/newdir/newfile': Operation not permitted
    dev-two@8baf87a55af1:/$ cat /var/tmp/newdir/newfile
    text

    Пробуем убрать sticky bit.

    8baf87a55af1# chmod 2775 /var/tmp/newdir
    8baf87a55af1# su - dev-two
    No directory, logging in with HOME=/
    dev-two@8baf87a55af1:/$ rm /var/tmp/newdir/newfile
    dev-two@8baf87a55af1:/$ ls -al /var/tmp/newdir/newfile
    ls: cannot access '/var/tmp/newdir/newfile': No such file or directory
    ```

- Создать директорию, в которой есть несколько файлов. Сделать так, чтобы открыть файлы можно только, зная имя файла, а через ls список файлов посмотреть нельзя.

    ```
    8baf87a55af1# mkdir /var/tmp/notshow
    8baf87a55af1# chmod a-r /var/tmp/notshow
    8baf87a55af1# echo "test" >/var/tmp/notshow/file
    8baf87a55af1# su - dev-one
    No directory, logging in with HOME=/
    dev-one@8baf87a55af1:/$ cat /var/tmp/notshow/file
    test
    dev-one@8baf87a55af1:/$ ls -la /var/tmp/notshow
    ls: cannot open directory '/var/tmp/notshow': Permission denied
    dev-one@8baf87a55af1:/$ ls -la /var/tmp/notshow/file
    -rw-r--r-- 1 root root 5 Oct 15 09:27 /var/tmp/notshow/file
    ```
