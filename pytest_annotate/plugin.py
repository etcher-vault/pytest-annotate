# Copyright 2017 Kensho Technologies, Inc.
"""The pytest plugin that calls out to PyAnnotate."""

import os

from pyannotate_runtime import collect_types


class PyAnnotatePlugin(object):
    """A pytest plugin that profiles function calls to extract type info."""

    def __init__(self, output_file):
        """Create a new PyAnnotatePlugin that analyzes function calls to extract type info."""
        self.output_file = output_file
        collect_types.init_types_collection()

    def pytest_unconfigure(self, config):
        """Unconfigure the pytest plugin. Happens when pytest is about to exit."""
        collect_types.dump_stats(self.output_file)

    def pytest_runtest_call(self):
        """Handle the pytest hook event that a test is about to be run: start type collection."""
        collect_types.resume()

    def pytest_runtest_teardown(self):
        """Handle the pytest test end hook event: stop type collection."""
        collect_types.pause()


def pytest_addoption(parser):
    """Add our --analyze option to the pytest option parser."""
    parser.addoption(
        '--annotate-output', help='Output file where PyAnnotate stats should be saved.')


def pytest_configure(config):
    """Configure the plugin based on the supplied value for the --annotate-output option."""
    option_value = config.getoption('--annotate-output')
    if option_value:
        base_path = os.path.abspath(option_value)
        config.pluginmanager.register(PyAnnotatePlugin(base_path))
