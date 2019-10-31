class Port(object):
    """
    Descriptor check port range,
    that must be in 1024-65535 range.
    """

    def __set_name__(self, owner, name):
        self.prop = name

    def __get__(self, instance, cls):
        return instance.__dict__.get(self.prop, None)

    def __set__(self, instance, value):
        """
        Check port range: must be not well known port:
        "The Well Known Ports are those from 0 through 1023".
        And must be less or qeual than 65535.
        """
        if 1023 > value or value > 65535:
            raise ValueError("port must contains value from range 1024-65535")
        instance.__dict__[self.prop] = value
