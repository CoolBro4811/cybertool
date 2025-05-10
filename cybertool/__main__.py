from pathlib import Path

import typer

from .config.loader import load_template, write_atomic
from .manager import PluginManager

app = typer.Typer()

# Where to look for plugins
PLUGIN_DIRS = [
    Path(__file__).parent / "plugins",
    Path(__file__).parent.parent / "plugins",
]
pm = PluginManager([p for p in PLUGIN_DIRS if p.exists()])


@app.command()
def list_plugins():
    """List all registered plugins"""
    for plugin in pm.pm.get_plugins():
        typer.echo(f"- {plugin.__name__}")


@app.command()
def apply_config(
    template: Path = typer.Option(..., help="Jinja2/YAML template (.j2)"),
    context_file: Path = typer.Option(None, help="Optional JSON context file"),
):
    """Render, run plugins, and write config"""
    ctx = {}
    if context_file:
        import json

        ctx = json.loads(context_file.read_text())

    cfg = load_template(str(template), ctx)
    pm.run_hook("before_apply", str(template))

    # Apply each plugin’s config_modify
    for modified in pm.run_hook("config_modify", cfg):
        if isinstance(modified, dict):
            cfg = modified

    out_path = str(template).rstrip(".j2")
    write_atomic(out_path, cfg)
    pm.run_hook("after_apply", out_path, True)


if __name__ == "__main__":
    app()
