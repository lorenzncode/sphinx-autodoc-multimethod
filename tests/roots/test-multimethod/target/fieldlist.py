from multimethod import multimethod


class Foo:
    """class docstring"""

    @multimethod
    def foobar(self, p1: int, p2: int) -> int:
        """
        Docstring on first method.

        :param p1: p1 definition
        :param p2: p2 definition
        """
        return 1

    @foobar.register
    def foobar(self, p1: bool, p2: bool) -> int:
        """
        more doc here
        """
        return 2
