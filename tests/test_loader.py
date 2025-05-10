import json
from pathlib import Path

from cybertool.config.loader import load_template, write_atomic


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
    assert cfg["enabled"] == True


def test_write_atomic(tmp_path):
    output = tmp_path / "out.yaml"
    data = {"foo": "bar"}
    write_atomic(str(output), data)

    assert output.exists()
    assert "foo" in output.read_text()
