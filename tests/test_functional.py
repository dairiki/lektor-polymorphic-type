# -*- coding: utf-8 -*-

import os
import pytest

from lektor.builder import Builder
from lektor.project import Project
from lektor.reporter import CliReporter

from lektor_polymorphic_type import PolymorphicTypePlugin


@pytest.fixture(scope='module')
def demo_output(tmp_path_factory):
    """ Build the demo site.

    Return path to output director.

    """
    site_dir = os.path.join(os.path.dirname(__file__), 'test-site')

    project = Project.from_path(site_dir)

    env = project.make_env(load_plugins=False)
    # Load our plugin
    env.plugin_controller.instanciate_plugin('polymorphic-type',
                                             PolymorphicTypePlugin)
    env.plugin_controller.emit('setup-env')

    output_path = tmp_path_factory.mktemp('output')
    builder = Builder(env.new_pad(), str(output_path))
    with CliReporter(env):
        failures = builder.build_all()
        assert failures == 0

    return output_path


def test_root_rendered_as_markdown(demo_output):
    root_html = demo_output / "index.html"
    assert '<p>This is a basic demo website' in root_html.read_text()


def test_about_rendered_as_text(demo_output):
    about_html = demo_output / "about/index.html"
    # check it was rendered
    assert 'This is a website' in about_html.read_text()
    # check there no markup
    assert '<p' not in about_html.read_text()
