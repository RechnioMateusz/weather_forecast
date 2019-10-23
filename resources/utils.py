from .errors import UtilsException


def average(list_):
    if not isinstance(list_, list):
        raise UtilsException(
            msg="Given parameter is not list", desc=f"It is {type(list_)}"
        )

    if list_:
        return sum(list_) / len(list_)

    return 0
