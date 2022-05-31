from multimethod import multimethod


class Foo:
    """class docstring"""

    @multimethod
    def meth(self, p1: int, p2: int):
        """Docstring on first method."""
        return 1

    @meth.register
    def meth(self, p1: str, p2: str):
        return 2
