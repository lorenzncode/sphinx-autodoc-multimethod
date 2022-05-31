"""Test without extension enabled for comparison."""

import pytest
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


@pytest.mark.sphinx("html", testroot="autodoc")
def test_no_ext_classmethod(app):
    # print(app.config.config_values)
    print(f"tmp = {app.config.autodoc_typehints}")
    print(f"tmp = {app.config.autodoc_typehints_description_target}")
    options = {"members": None}
    actual = do_autodoc(app, "module", "target.classmethod", options)
    assert list(actual) == [
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
        "   .. py:method:: Foo.foobar(p1) -> " "~target.classmethod.Foo",
        "      :module: target.classmethod",
        "      :classmethod:",
        "",
        "      foobar docstring",
        "",
        "",
        "   .. py:method:: Foo.foobar_cls_typehint(p1: int) -> "
        "~target.classmethod.Foo",
        "      :module: target.classmethod",
        "      :classmethod:",
        "",
        "      foobar_cls_typehint docstring",
        "",
        "",
        "   .. py:method:: Foo.foobar_param_typehint(p1: int) -> "
        "~target.classmethod.Foo",
        "      :module: target.classmethod",
        "      :classmethod:",
        "",
        "      foobar_param_typehint docstring",
        "",
        "",
        "   .. py:method:: Foo.foobar_typehint_docparam(p1: int) -> "
        "~target.classmethod.Foo",
        "      :module: target.classmethod",
        "      :classmethod:",
        "",
        "      docstring",
        "",
        "      :param p1: p1 definition",
        "",
    ]
