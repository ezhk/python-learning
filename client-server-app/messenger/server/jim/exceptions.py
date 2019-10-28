class MessageError(Exception):
    def __init__(self, error, *args, **kwargs):
        self.error = error
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{super().__str__()} ошибка в сообщении, {self.error}"
