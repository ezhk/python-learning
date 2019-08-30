class ResponseCodeError(Exception):
    def __init__(self, code, *args, **kwargs):
        self.code = code
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{super().__str__()} некорректный код ответа, {self.code}"


class MessageError(Exception):
    def __init__(self, error, *args, **kwargs):
        self.error = error
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{super().__str__()} ошибка в сообщении, {self.error}"


class UsernameError(Exception):
    def __init__(self, username, *args, **kwargs):
        self.username = username
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{super().__str__()} некорректное имя пользователя, {self.username}"
