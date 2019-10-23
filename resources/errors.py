class AbstractException(Exception):
    """Abstract exception to inherit from.

    **Attributes**
        :msg: Exception message. [str]
        :desc: Exception description. [str]
    """

    def __init__(self, msg, desc=None):
        """Constructor for 'AbstractException' exception.

        **Args**
            :msg: Exception message. [str]
        **Kwargs**
            :desc: Exception description. [str]
        """

        super().__init__(msg)
        self.msg = msg
        self.desc = desc

    def __str__(self):
        return f"Message: {self.msg}\nDescription: {self.desc}"


class AdapterException(AbstractException):
    """Exception for adapters."""


class FactoryException(AbstractException):
    """Exception for factoires."""


class UtilsException(AbstractException):
    """Exception for utilities."""
