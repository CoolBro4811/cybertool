import json
from pathlib import Path

from typer.testing import CliRunner

from cybertool.__main__ import app

runner = CliRunner()


def test_list_plugins():
    result = runner.invoke(app, ["list-plugins"])
    assert result.exit_code == 0
    assert "example_plugin" in result.output


def test_apply_config(tmp_path):
    tpl = tmp_path / "ssh_config.j2"
    tpl.write_text("PermitRootLogin: {{ root }}\n")

    ctx = tmp_path / "ctx.json"
    ctx.write_text(json.dumps({"root": "no"}))

    result = runner.invoke(
        app,
        ["apply-config", "--template", str(tpl), "--context-file", str(ctx)],
    )

    out_file = str(tpl).rstrip(".j2")
    assert Path(out_file).exists()
    assert "PermitRootLogin: no" in Path(out_file).read_text()
