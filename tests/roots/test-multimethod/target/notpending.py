from multimethod import multimethod


class Foo(object):

    """class docstring"""

    @multimethod
    def foobar(cls, p1: int, p2: int) -> "Foo":
        """
        Docstring on first method.

        :param p1: p1 definition
        :param p2: p2 definition
        """

        return cls()

    @classmethod
    @foobar.register
    def foobar(cls, p1: float, p2: float) -> "Foo":

        return cls()

    @multimethod
    def foobar2(self, p1: int, p2: int) -> int:
        """
        Docstring on first method.

        :param p1: p1 definition
        :param p2: p2 definition
        """

        return 1

    @foobar2.register
    def foobar2(self, p1: float, p2: float) -> int:

        return 1

    @multimethod
    def foobar3(p1: int, p2: int) -> int:
        """
        Docstring on first method.

        :param p1: p1 definition
        :param p2: p2 definition
        """

        return 1

    @staticmethod
    @foobar3.register
    def foobar3(p1: str, p2: str) -> int:

        return 1


Foo().foobar(1, 2)
Foo().foobar(1.0, 2.0)

a = Foo()
a.foobar2(1, 2)
a.foobar2(1.0, 2.0)

Foo().foobar3(1, 2)
Foo().foobar3("a", "b")
