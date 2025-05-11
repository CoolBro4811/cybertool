import sys
import textwrap
from pathlib import Path

from cybertool.config.loader import load_template, write_atomic
from cybertool.hookspecs import hookimpl, hookspec
from cybertool.manager import PluginManager


def test_template_loading_and_rendering(tmp_path):
    tpl_path = tmp_path / "config.yaml.j2"
    tpl_path.write_text(
        """
port: {{ port }}
enabled: true
"""
    )

    context = {"port": 2222}
    cfg = load_template(str(tpl_path), context)

    assert cfg["port"] == 2222
    assert cfg["enabled"] is True


def test_write_atomic(tmp_path):
    output = tmp_path / "out.yaml"
    data = {"foo": "bar", "testing 1 2 3 \n\n\n": False}

    write_atomic(str(output), data)

    assert output.exists()
    assert "foo" in output.read_text()
    assert "false" in output.read_text()


def test_dynamic_plugin_file_loading(tmp_path):
    # create a plugin file
    plug_dir = tmp_path / "plugins"
    plug_dir.mkdir()
    plugin_py = plug_dir / "test_dyn.py"
    plugin_py.write_text(
        textwrap.dedent(
            """
        from cybertool.hookspecs import hookimpl, hookspec

        @hookimpl
        @hookspec
        def config_modify(config):
            config["loaded"] = 123
            return config
    """
        )
    )

    pm = PluginManager([plug_dir])
    cfg = {}
    out = pm.run_hook("config_modify", config=cfg)
    assert out == [{"loaded": 123}]
