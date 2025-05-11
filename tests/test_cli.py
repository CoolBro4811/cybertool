import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cybertool.__main__ import app
from cybertool.utils import validate_ssh_config

runner = CliRunner()


def test_list_plugins():
    result = runner.invoke(app, ["list-plugins"])
    assert result.exit_code == 0
    print(result.output)
    assert "Registered Plugins:" in result.output
    assert "ssh_hardening" in result.output
    assert "example_plugin" in result.output
    # ... could add more if needed


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


class DummyProc:
    def __init__(self, rc):
        self.rc = rc

    def run(self, *args, **kwargs):
        if self.rc != 0:
            raise subprocess.CalledProcessError(1, args[0])


def test_validate_ssh_config_success(monkeypatch):
    monkeypatch.setattr(
        subprocess, "run", lambda *args, **kw: DummyProc(0).run()
    )
    assert validate_ssh_config("/fake/path") is True


def test_validate_ssh_config_failure(monkeypatch):
    def fakerrun(cmd, check):
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(subprocess, "run", fakerrun)
    assert validate_ssh_config("/fake/path") is False
