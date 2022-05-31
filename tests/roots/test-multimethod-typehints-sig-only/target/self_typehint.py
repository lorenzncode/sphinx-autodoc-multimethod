from multimethod import multimethod

from typing import TypeVar

T = TypeVar("T", bound="Foo")


class Foo:

    """class docstring"""

    @multimethod
    def foobar(self: T, p1: int, p2: int) -> T:
        """
        Docstring on first method.

        :param p1: p1 definition
        :param p2: p2 definition
        """
        return self

    @foobar.register
    def foobar(self: T, p1: bool, p2: bool) -> T:
        """
        more doc here
        """
        return self
