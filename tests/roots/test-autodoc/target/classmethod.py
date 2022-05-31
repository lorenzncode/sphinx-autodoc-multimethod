from typing import TypeVar

T = TypeVar("T", bound="Foo")


class Foo(object):
    """class docstring"""

    @classmethod
    def foobar(cls, p1) -> "Foo":
        """foobar docstring"""

        return cls()

    @classmethod
    def foobar_cls_typehint(cls, p1: int) -> "Foo":
        """foobar_cls_typehint docstring"""

        return cls()

    @classmethod
    def foobar_param_typehint(cls, p1: int) -> "Foo":
        """foobar_param_typehint docstring"""

        return cls()

    @classmethod
    def foobar_typehint_docparam(cls, p1: int) -> "Foo":
        """docstring

        :param p1: p1 definition
        """

        return cls()
