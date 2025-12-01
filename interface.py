# -*- coding: utf-8 -*-
"""
:copyright: Nokia Networks
:author: Rashmi R
:contact: rashmi.r@nokia.com
:maintainer: Rashmi R
:contact: rashmi.r@nokia.com

Helper keywords for managing Robot Framework variable aliases across different
scopes. The original metadata is kept for traceability.
"""

from robot.libraries.BuiltIn import BuiltIn
import logging


class store(object):
    """Expose convenience keywords for alias creation and scoping."""

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    _namespace = "aliasstore"

    def __init__(self, **kwargs):
        """Instantiate the library and cache the BuiltIn interface."""
        super(store, self).__init__(**kwargs)
        self._builtin = self._create_builtin()

    def _create_builtin(self):
        """Do not import BuiltIn at module import time to simplify mocking."""
        return BuiltIn()

    def set_alias(self, alias, obj):
        """Store the given Python object under an alias in Robot variables."""
        if "::" not in alias:
            alias = "::".join([self._namespace, alias])
        self._builtin._variables["${%s}" % alias] = obj

    def get_alias_value(self, alias):
        """Return the stored alias value, warning if it does not exist."""
        if "::" not in alias:
            alias = "::".join([self._namespace, alias])
        value = self._builtin.get_variable_value("${%s}" % alias)
        if value is None:
            logging.warning(
                "Alias {alias!r} is not defined. "
                "Hint: After calling a create keyword, which uses an alias, you often need to set the scope"
                " of the alias, e. g. via set_suite_alias(). "
                "See https://confluence.ext.net.nokia.com/display/CV/_Collector+Concepts#id-_CollectorConcepts-"
                "AliasScopes".format(alias=alias))
        return value

    def set_suite_alias(self, alias):
        """Promote the alias to suite scope."""
        if "::" not in alias:
            alias = "::".join([self._namespace, alias])
        self._builtin.set_suite_variable("${%s}" % alias)

    def set_test_alias(self, alias):
        """Restrict the alias to test-case scope."""
        if "::" not in alias:
            alias = "::".join([self._namespace, alias])
        self._builtin.set_test_variable("${%s}" % alias)

    def set_global_alias(self, alias):
        """Promote the alias to global scope."""
        if "::" not in alias:
            alias = "::".join([self._namespace, alias])
        self._builtin.set_global_variable("${%s}" % alias)

    def set_scope(self, alias, scope):
        """Map a textual scope to the matching Robot alias setter."""
        if scope == "global":
            self.set_global_alias(alias)
        elif scope == "suite":
            self.set_suite_alias(alias)
        elif scope == "test":
            self.set_test_alias(alias)
