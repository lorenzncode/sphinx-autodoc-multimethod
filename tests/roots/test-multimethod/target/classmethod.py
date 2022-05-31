from multimethod import multimethod
from typing import TypeVar

T = TypeVar("T", bound="Foo")


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
    def foobar(cls, p1: bool, p2: bool) -> "Foo":

        return cls()

    @multimethod
    def foobar2(cls, p1: int, p2: int) -> "Foo":
        """
        Docstring on first method.

        """
        return cls()

    @classmethod
    @foobar2.register
    def foobar2(cls, p1: bool, p2: bool) -> "Foo":

        return cls()

    @classmethod
    def foobar3(cls, p1) -> "Foo":
        """foobar3 docstring"""

        return cls()

    @classmethod
    def foobar4(cls, p1: int) -> "Foo":
        """foobar4 docstring"""

        return cls()
