""" 
Check that the extension does not break autodoc handling of e.g. singledispatch
Selected tests from sphinx test_ext_autodoc.py
"""

import pytest
import sys
from unittest.mock import Mock

from sphinx.ext.autodoc.directive import DocumenterBridge, process_documenter_options
from sphinx.util.docutils import LoggingReporter


def do_autodoc(app, objtype, name, options=None):
    if options is None:
        options = {}
    app.env.temp_data.setdefault("docname", "index")  # set dummy docname
    doccls = app.registry.documenters[objtype]
    docoptions = process_documenter_options(doccls, app.config, options)
    state = Mock()
    state.document.settings.tab_width = 8
    bridge = DocumenterBridge(app.env, LoggingReporter(""), docoptions, 1, state)
    documenter = doccls(bridge, name)
    documenter.generate()

    return bridge.result


@pytest.mark.skipif(
    sys.version_info < (3, 8),
    reason="singledispatchmethod is available since python3.8",
)
@pytest.mark.sphinx("html", testroot="functools")
def test_singledispatch(app):
    options = {"members": None}
    actual = do_autodoc(app, "module", "target.singledispatch", options)
    assert list(actual) == [
        "",
        ".. py:module:: target.singledispatch",
        "",
        "",
        ".. py:function:: func(arg, kwarg=None)",
        "                 func(arg: float, kwarg=None)",
        "                 func(arg: int, kwarg=None)",
        "                 func(arg: str, kwarg=None)",
        "   :module: target.singledispatch",
        "",
        "   A function for general use.",
        "",
    ]


@pytest.mark.skipif(
    sys.version_info < (3, 8),
    reason="singledispatchmethod is available since python3.8",
)
@pytest.mark.sphinx("html", testroot="functools")
def test_singledispatchmethod(app):
    options = {"members": None}
    actual = do_autodoc(app, "module", "target.singledispatchmethod", options)
    assert list(actual) == [
        "",
        ".. py:module:: target.singledispatchmethod",
        "",
        "",
        ".. py:class:: Foo()",
        "   :module: target.singledispatchmethod",
        "",
        "   docstring",
        "",
        "",
        "   .. py:method:: Foo.meth(arg, kwarg=None)",
        "                  Foo.meth(arg: float, kwarg=None)",
        "                  Foo.meth(arg: int, kwarg=None)",
        "                  Foo.meth(arg: str, kwarg=None)",
        "      :module: target.singledispatchmethod",
        "",
        "      A method for general use.",
        "",
    ]


@pytest.mark.skipif(
    sys.version_info < (3, 8),
    reason="singledispatchmethod is available since python3.8",
)
@pytest.mark.sphinx("html", testroot="functools")
def test_singledispatchmethod_automethod(app):
    options = {}
    actual = do_autodoc(app, "method", "target.singledispatchmethod.Foo.meth", options)
    assert list(actual) == [
        "",
        ".. py:method:: Foo.meth(arg, kwarg=None)",
        "               Foo.meth(arg: float, kwarg=None)",
        "               Foo.meth(arg: int, kwarg=None)",
        "               Foo.meth(arg: str, kwarg=None)",
        "   :module: target.singledispatchmethod",
        "",
        "   A method for general use.",
        "",
    ]
