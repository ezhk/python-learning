# Скрипты

* Написать скрипт, который удаляет из текстового файла пустые строки и заменяет маленькие символы на большие (воспользуйтесь tr или sed).

    ```
    sed -e '/^\s*$/d' filename | tr "a-z" "A-Z"
    ```

* Создать скрипт, который создаст директории для нескольких годов (2010 — 2017), в них — поддиректории для месяцев (от 01 до 12), и в каждый из них запишет несколько файлов с произвольными записями (например 001.txt, содержащий текст Файл 001, 002.txt с текстом Файл 002) и т.д.

    ```
    #!/bin/bash

    mkdir tmp
    seq 2010 2017 | while read year
    do
        seq 1 12 | while read monthseq
        do
            month=${monthseq}
            if [ ${monthseq} -lt 10 ]
            then
                month="0${monthseq}"
            fi

            mkdir -p "tmp/${year}/${month}"
            echo "001" >tmp/${year}/${month}/001.txt
            echo "002" >tmp/${year}/${month}/002.txt
        done
    done
    ```

# Более сложные задания на скрипты (и cron)

* Создать файл crontab, который ежедневно регистрирует занятое каждым пользователем дисковое пространство в его домашней директории.

    ```
    SHELL=/bin/bash

    # run script every nigth at 1AM
    0  1   *   *   *   root   /usr/bin/du -hd1 /home/* &>>/var/log/homedir-size.log
    ```

* Создать скрипт ownersort.sh, который в заданной папке копирует файлы в директории, названные по имени владельца каждого файла. Учтите, что файл должен принадлежать соответствующему владельцу

    ```
    #!/bin/bash
    mkdir tmp

    find /home -type f | while read fname
    do
        username=$(stat -c "%U" ${fname})
        test -d tmp/${username} || mkdir -p tmp/${username}

        # copy with preserve mode enabled
        cp -p ${fname} tmp/${username}
    done
    ```

* Написать скрипт rename.sh, аналогичный разобранному, но порядковые номера файлов выравнивать, заполняя слева нуля до ширины максимального значения индекса: newname000.jpg, newname102.jpg (Использовать printf). Дополнительно к 3 добавить проверку на расширение, чтобы не переименовать .sh.

    ```
    #!/bin/bash
    max_value=$(find . -name "newname*" | grep -Po "(\d+)(?=\.\w+$)" | sort -rn | head -n1)
    max_len=$(expr length ${max_value})

    find . -name "newname*" -type f | while read fname
    do
        cur_value=$(echo ${fname} | grep -Po "(\d+)(?=\.\w+$)")
        test -z "${cur_value}" && continue

        new_value=${cur_value}
        while [ $(expr length "${new_value}") != ${max_len} ]
        do
            new_value="0${new_value}"
        done

        new_fname=$(echo ${fname} | sed -r "s/${cur_value}(\.\w+)$/${new_value}\1/g")
        test "${fname}" != "${new_fname}" && mv ${fname} ${new_fname}
    done
    ```

* Написать скрипт резервного копирования по расписанию следующим образом:
В первый день месяца помещать копию в backdir/montlhy.
Бэкап по пятницам хранить в каталоге backdir/weekley.
В остальные дни сохранять копии в backdir/daily.
Настроить ротацию следующим образом. Ежемесячные копии хранить 180 дней, ежедневные — неделю, еженедельные — 30 дней. Подсказка: для ротации используйте find.

    ```
    SKIP
    ```

* Написать скрипт мониторинга лога, используя утилиту tailf, чтобы он выводил сообщения при попытке неудачной аутентификации пользователя /var/log/auth.log, отслеживая сообщения примерно такого вида:
    ```
    May 16 19:45:52 vlamp login[102782]: FAILED LOGIN (1) on '/dev/tty3' FOR 'user', Authentication failure
    ```
    Проверить скрипт, выполнив ошибочную регистрацию с виртуального терминала.
    ```
    SKIP: tailf is deprecated and doesn't exit in Ubuntu Bionic.
    ```
