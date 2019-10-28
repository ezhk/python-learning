import dis


def is_incorrect_methods(instruction, incorrect_methods):
    return (
        instruction.opname == "LOAD_METHOD"
        and instruction.argrepr in incorrect_methods
    )


class ServerVerifier(type):
    """
    Metaclass verify:

    - class doesn't contain connect call in methods
    - class contains "SOCK_STREAM" and "AF_INET" in global import,
      but doesn't validate, that these constans will be used
    """

    INCORRECT_METHODS = ("connect",)
    IMPORT_GLOBAL = set(["SOCK_STREAM", "AF_INET"])

    def __init__(self, name, bases, attrs):
        load_global = set()
        for f_name, f_call in attrs.items():
            try:
                for instruction in dis.get_instructions(f_call):
                    if is_incorrect_methods(
                        instruction, self.INCORRECT_METHODS
                    ):
                        raise RuntimeError(
                            f"Server cannot calls {self.INCORRECT_METHODS} methods"
                        )

                    if instruction.opname == "LOAD_GLOBAL":
                        load_global.add(instruction.argrepr)
            except TypeError:
                pass

        # it's enought check only once, because for client this metaclass called too.
        if self.IMPORT_GLOBAL - load_global:
            raise RuntimeError(
                f"Const {self.IMPORT_GLOBAL} doesn't import globally"
            )

        super().__init__(name, bases, attrs)
