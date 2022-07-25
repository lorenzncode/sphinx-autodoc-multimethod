import pytest
import re
from itertools import groupby
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


def max_empty_lines(lines, n: int = 2):
    """Allow maximum of n consecutive empty lines to be insensive to small changes in whitespace.
    Found difference with multimethod 1.6 vs 1.8.
    """

    lines_replace = []
    for k, g in groupby(lines, lambda l: not (l.strip())):
        g = list(g)
        if g[0] == "" and len(g) > n:
            lines_replace.extend(g[0:n])
        else:
            lines_replace.extend(g)

    return lines_replace


@pytest.mark.sphinx("html", testroot="multimethod")
def test_multimethod(app):
    options = {"members": None}
    actual = do_autodoc(app, "module", "target.multi", options)
    # actual = max_empty_lines(actual)
    assert list(actual)[0:10] == [
        "",
        ".. py:module:: target.multi",
        "",
        "",
        ".. py:class:: Foo()",
        "   :module: target.multi",
        "",
        "   class docstring",
        "",
        "",
    ]
    assert re.match(r"   .. py:method:: Foo.meth\(p1: \w+, p2: \w+\)", actual[10])
    assert re.match(r"                  Foo.meth\(p1: \w+, p2: \w+\)", actual[11])
    assert list(actual)[12:16] == [
        "      :module: target.multi",
        "",
        "      Docstring on first method.",
        "",
    ]


@pytest.mark.sphinx("html", testroot="multimethod")
def test_multimethod_fieldlist(app):
    options = {"members": None}
    actual = do_autodoc(app, "module", "target.fieldlist", options)
    assert list(actual)[0:10] == [
        "",
        ".. py:module:: target.fieldlist",
        "",
        "",
        ".. py:class:: Foo()",
        "   :module: target.fieldlist",
        "",
        "   class docstring",
        "",
        "",
    ]
    assert re.match(
        r"   .. py:method:: Foo.foobar\(p1: \w+, p2: \w+\) -> int", actual[10]
    )
    assert re.match(
        r"                  Foo.foobar\(p1: \w+, p2: \w+\) -> int", actual[11]
    )
    assert list(actual)[12:] == [
        "      :module: target.fieldlist",
        "",
        "      Docstring on first method.",
        "",
        "      :param p1: p1 definition",
        "      :param p2: p2 definition",
        "",
        "",
        "",
        "",
        "      more doc here",
        "",
        "",
    ]


@pytest.mark.sphinx("html", testroot="multimethod")
def test_multiline_param_desc(app):
    options = {"members": None}
    actual = do_autodoc(app, "module", "target.multiline_param_desc", options)
    assert list(actual)[0:10] == [
        "",
        ".. py:module:: target.multiline_param_desc",
        "",
        "",
        ".. py:class:: Foo()",
        "   :module: target.multiline_param_desc",
        "",
        "   class docstring",
        "",
        "",
    ]
    assert re.match(
        r"   .. py:method:: Foo.foobar\(p1: \w+, p2: \w+\) -> int", actual[10]
    )
    assert re.match(
        r"                  Foo.foobar\(p1: \w+, p2: \w+\) -> int", actual[11]
    )
    assert list(actual)[12:] == [
        "      :module: target.multiline_param_desc",
        "",
        "      Docstring on first method.",
        "",
        "      :param p1: p1 definition",
        "      :param p2: long p2 definition that continues",
        "                 on next line",
        "",
        "",
        "",
        "",
        "      more doc here",
        "",
        "",
    ]


@pytest.mark.skip(
    reason="customization to insert self removed, if needed add to a separate autodoc-process-docstring event"
)
@pytest.mark.sphinx("html", testroot="multimethod")
def test_multimethod_insert_self(app):
    options = {"members": None}
    actual = do_autodoc(app, "module", "target.self_typehint", options)
    assert list(actual)[0:10] == [
        "",
        ".. py:module:: target.self_typehint",
        "",
        "",
        ".. py:class:: Foo()",
        "   :module: target.self_typehint",
        "",
        "   class docstring",
        "",
        "",
    ]
    assert re.match(
        r"   .. py:method:: Foo.foobar\(p1: \w+, p2: \w+\) -> ~target.self_typehint.T",
        actual[10],
    )
    assert re.match(
        r"                  Foo.foobar\(p1: \w+, p2: \w+\) -> ~target.self_typehint.T",
        actual[11],
    )
    assert list(actual)[12:] == [
        "      :module: target.self_typehint",
        "",
        "      Docstring on first method.",
        "",
        "      :param self:",
        "      :param p1: p1 definition",
        "      :param p2: p2 definition",
        "",
        "",
        "",
        "",
        "      more doc here",
        "",
        "",
    ]


@pytest.mark.sphinx("html", testroot="multimethod")
def test_multimethod_classmethod(app):
    options = {"members": None}
    actual = do_autodoc(app, "module", "target.classmethod", options)
    assert list(actual)[0:10] == [
        "",
        ".. py:module:: target.classmethod",
        "",
        "",
        ".. py:class:: Foo()",
        "   :module: target.classmethod",
        "",
        "   class docstring",
        "",
        "",
    ]
    assert re.match(
        r"   .. py:method:: Foo.foobar\(p1: \w+, p2: \w+\) -> ~target.classmethod.Foo",
        actual[10],
    )
    assert re.match(
        r"                  Foo.foobar\(p1: \w+, p2: \w+\) -> ~target.classmethod.Foo",
        actual[11],
    )
    assert list(actual)[12:21] == [
        "      :module: target.classmethod",
        "      :classmethod:",
        "",
        "      Docstring on first method.",
        "",
        "      :param p1: p1 definition",
        "      :param p2: p2 definition",
        "",
        "",
    ]
    assert re.match(
        r"   .. py:method:: Foo.foobar2\(p1: \w+, p2: \w+\) -> ~target.classmethod.Foo",
        actual[21],
    )
    assert re.match(
        r"                  Foo.foobar2\(p1: \w+, p2: \w+\) -> ~target.classmethod.Foo",
        actual[22],
    )
    assert list(actual)[23:25] == [
        "      :module: target.classmethod",
        "      :classmethod:",
    ]
    assert list(actual)[25:43] == [
        "",
        "      Docstring on first method.",
        "",
        "",
        "",
        "   .. py:method:: Foo.foobar3(p1) -> ~target.classmethod.Foo",
        "      :module: target.classmethod",
        "      :classmethod:",
        "",
        "      foobar3 docstring",
        "",
        "",
        "   .. py:method:: Foo.foobar4(p1: int) -> ~target.classmethod.Foo",
        "      :module: target.classmethod",
        "      :classmethod:",
        "",
        "      foobar4 docstring",
        "",
    ]


@pytest.mark.sphinx("html", testroot="multimethod")
def test_multimethod_staticmethodnew(app):
    options = {"members": None}
    actual = do_autodoc(app, "module", "target.staticmethod", options)
    actual = max_empty_lines(actual)
    assert actual[0:10] == [
        "",
        ".. py:module:: target.staticmethod",
        "",
        "",
        ".. py:class:: Foo()",
        "   :module: target.staticmethod",
        "",
        "   class docstring",
        "",
        "",
    ]
    assert re.match(
        r"   .. py:method:: Foo.foobar\(p1: \w+, p2: \w+\) -> int", actual[10]
    )
    assert re.match(
        r"                  Foo.foobar\(p1: \w+, p2: \w+\) -> int", actual[11]
    )
    assert re.match(
        r"                  Foo.foobar\(p1: \w+, p2: \w+\) -> int", actual[12]
    )
    assert actual[13:19] == [
        "      :module: target.staticmethod",
        "      :staticmethod:",
        "",
        "      Docstring on first method.",
        "",
        "",
    ]
    assert re.match(
        r"   .. py:method:: Foo.foobar_param\(p1: \w+, p2: \w+\) -> int", actual[19]
    )
    assert re.match(
        r"                  Foo.foobar_param\(p1: \w+, p2: \w+\) -> int", actual[20]
    )
    assert re.match(
        r"                  Foo.foobar_param\(p1: \w+, p2: \w+\) -> int", actual[21]
    )
    assert list(actual)[22:30] == [
        "      :module: target.staticmethod",
        "      :staticmethod:",
        "",
        "      Docstring on first method.",
        "",
        "      :param p1: p1 definition",
        "      :param p2: p2 definition",
        "",
    ]


@pytest.mark.sphinx("html", testroot="multimethod")
def test_multimethod_notpending(app):
    options = {"members": None}
    actual = do_autodoc(app, "module", "target.notpending", options)
    actual = max_empty_lines(actual)
    assert list(actual)[0:10] == [
        "",
        ".. py:module:: target.notpending",
        "",
        "",
        ".. py:class:: Foo()",
        "   :module: target.notpending",
        "",
        "   class docstring",
        "",
        "",
    ]
    assert re.match(r"   .. py:method:: Foo.foobar\(p1: \w+, p2: \w+\)", actual[10])
    assert re.match(r"                  Foo.foobar\(p1: \w+, p2: \w+\)", actual[11])
    assert list(actual)[12:21] == [
        "      :module: target.notpending",
        "      :classmethod:",
        "",
        "      Docstring on first method.",
        "",
        "      :param p1: p1 definition",
        "      :param p2: p2 definition",
        "",
        "",
    ]
    assert re.match(r"   .. py:method:: Foo.foobar2\(p1: \w+, p2: \w+\)", actual[21])
    assert re.match(r"                  Foo.foobar2\(p1: \w+, p2: \w+\)", actual[22])
    assert list(actual)[23:31] == [
        "      :module: target.notpending",
        "",
        "      Docstring on first method.",
        "",
        "      :param p1: p1 definition",
        "      :param p2: p2 definition",
        "",
        "",
    ]
    assert re.match(r"   .. py:method:: Foo.foobar3\(p1: \w+, p2: \w+\)", actual[31])
    assert re.match(r"                  Foo.foobar3\(p1: \w+, p2: \w+\)", actual[32])
    assert list(actual)[33:41] == [
        "      :module: target.notpending",
        "      :staticmethod:",
        "",
        "      Docstring on first method.",
        "",
        "      :param p1: p1 definition",
        "      :param p2: p2 definition",
        "",
    ]


@pytest.mark.sphinx("html", testroot="multimethod-typehints-sig-only")
def test_multimethod_documented_params(app):
    options = {"members": None}
    actual = do_autodoc(app, "module", "target.self_typehint", options)
    assert list(actual)[0:10] == [
        "",
        ".. py:module:: target.self_typehint",
        "",
        "",
        ".. py:class:: Foo()",
        "   :module: target.self_typehint",
        "",
        "   class docstring",
        "",
        "",
    ]
    assert re.match(r"   .. py:method:: Foo.foobar\(p1: \w+, p2: \w+\)", actual[10])
    assert re.match(r"                  Foo.foobar\(p1: \w+, p2: \w+\)", actual[11])
    assert list(actual)[12:] == [
        "      :module: target.self_typehint",
        "",
        "      Docstring on first method.",
        "",
        "      :param p1: p1 definition",
        "      :param p2: p2 definition",
        "",
        "",
        "",
        "",
        "      more doc here",
        "",
        "",
    ]
