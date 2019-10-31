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

- переходитм директорию server
- создаем в директории messenger БД(sqlite):  
```
>>> from jim.server_models import create_db
>>> create_db()
```

- запускаем серверную часть: ```./server.py```

## Client-side

- переходим в директорию client
- запускаем клиентскую часть с каким-то именем и паролем: ```./client.py -u John -P test```
- запускаем ещё одну клиентскую часть: ```./client.py -u Ann -P test```

Если пароль или имя пользователя не ввести, то появится диалоговое окно  
где необходимо будет ввести эти данные.  
  
Теперь в любой из клиентских частей мы можем отправлять сообщения  
перейдя в соответствующий чат с необходимым пользователем.

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
