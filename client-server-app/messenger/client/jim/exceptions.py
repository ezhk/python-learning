class UsernameError(Exception):
    """
    Exception might be called when
    wrong username has been typed.
    """

    def __init__(self, username, *args, **kwargs):
        self.username = username
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{super().__str__()} некорректное имя пользователя, {self.username}"
