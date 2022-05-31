from multimethod import multimethod


class Foo:
    """class docstring"""

    @multimethod
    def foobar(p1: int, p2: int) -> int:
        """
        Docstring on first method.
        """
        return 1

    @foobar.register
    def foobar(p1: str, p2: str) -> int:

        return 2

    @staticmethod
    @foobar.register
    def foobar(p1: bool, p2: bool) -> int:

        return 3

    @multimethod
    def foobar_param(p1: int, p2: int) -> int:
        """
        Docstring on first method.

        :param p1: p1 definition
        :param p2: p2 definition
        """
        return 1

    @foobar_param.register
    def foobar_param(p1: str, p2: str) -> int:

        return 2

    @staticmethod
    @foobar_param.register
    def foobar_param(p1: bool, p2: bool) -> int:

        return 3
