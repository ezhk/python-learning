# README
Все файлы должны выполняться в директорях server или client,  
в зависимости от того, какую часть мессенжера вы запускаете.  
Поскольку внутри скриптов есть добавление sys path  
для поиска библиотек ".".

Для тестирования файлов аналогично надо запускать в
директории client или server, не test, например:
```python tests/test_logger.py```


# Проверка работы CLI части

- устанавливаем необходимые зависимости:
```pip install -r requirements.txt```

## Server-side

- подготоваливаем работу с MongoDB:

        $ docker run --name messenger-mongo \
            -e MONGO_INITDB_ROOT_USERNAME=root \
            -e MONGO_INITDB_ROOT_PASSWORD=0Kk3KVDbR0BVKzPUodjw \
            -p 27017:27017 -d mongo

        $ docker exec -ti messenger-mongo mongo -u root -p 0Kk3KVDbR0BVKzPUodjw
            > use messenger
            > db.createUser({user: "root", pwd: "0Kk3KVDbR0BVKzPUodjw", roles:[{role: "dbOwner" , db:"messenger"}]})

- переходим директорию server
- проверяем настроки для соединения с базой данных в jim/config.py — ```STORAGE```
- запускаем серверную часть: ```./server.py```

Первая загрузка серверной части:

- будет достаточно долгой, если включен ENABLE_FILTER в jim/config.py (по умолчанию `False`):

    причиной тому использование библиотеки profanity_check,  
    которая помогает фильтровать сообщения на нецензурные английские слова.

- в директории server будет создана база данных со структурой из utils/models.py.  

Для работы серверной части остается запустить сервер,  
нажав кнопку Run server.
  
По умолчанию заведены пользователи:

- John, пароль test, в друзьях Ann и test, и группы #all и #friends
- Ann, пароль test, в друзьях только John и группа #friends
- test, пароль test, в друзьях только John и группа #all


## Client-side

- переходим в директорию client
- запускаем клиентскую часть с каким-то именем и паролем: ```./client.py -u John -P test```;  
  в качествe альтернативы появилась возможность использовать в качестве клиента kv-client.py,  
  для этого достаточно запустить ```./kv-client.py```.
- запускаем ещё одну клиентскую часть: ```./client.py -u Ann -P test```

Если пароль или имя пользователя не ввести, то появится диалоговое окно  
где необходимо будет ввести эти данные.  
  
Теперь в любой из клиентских частей мы можем отправлять сообщения  
перейдя в соответствующий чат с необходимым пользователем.  
  
Если указанного пользователя нет в базе данных,  
то он создастся с введенным паролем.  
  
Также есть возможность изменять аватар пользователя:  
для этого достаточно кликнуть на изображение пользователя  
и появится возможность выбрать, обрезать изображение и  
сохранить его в БД.

# Upload пакетов в репозиторий

Созаем `~/.pypirc`

    [distutils]
    index-servers=
        pypi

    [pypi]
    repository: https://upload.pypi.org/legacy/
    username: username

    [testpypi]
    repository: https://testpypi.python.org/pypi
    username: username

Собираем и заливаем в репозиторий:

```
$ python setup.py clean bdist_wheel
$ twine upload dist/*
```
