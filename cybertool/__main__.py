from pathlib import Path

import typer

from .config.loader import load_template, write_atomic
from .manager import PluginManager

app = typer.Typer()

PLUGIN_DIRS = [
    Path(__file__).parent / "plugins",
    Path(__file__).parent.parent / "plugins",
]
pm = PluginManager([p for p in PLUGIN_DIRS if p.exists()])


@app.command()
def list_plugins():
    """List all registered plugins"""
    typer.echo("Registered Plugins:\n")

    for name, plugin in pm.pm._name2plugin.items():
        typer.echo(f"- Name: {name}")
        typer.echo(f"   Class: {plugin.__class__.__name__}")
        typer.echo("    Implements:")

        hooks = []
        for hook_name in pm.pm.hook.__dict__:
            hook_func = getattr(pm.pm.hook, hook_name)
            hook_callers = hook_func.get_hookimpls()
            for impl in hook_callers:
                if impl.plugin == plugin:
                    hooks.append(hook_name)

        if hooks:
            for h in hooks:
                typer.echo(f"   - {h}")
        else:
            typer.echo("    (no hooks implemented)")

        typer.echo("")  # spacing, might change later


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
    result = pm.run_hook("before_apply", target=str(template))

    # Apply each plugin’s config_modify
    for modified in pm.run_hook("config_modify", config=cfg):
        if isinstance(modified, dict):
            cfg = modified

    out_path = str(template).rstrip(".j2")
    write_atomic(out_path, cfg)
    pm.run_hook("after_apply", target=out_path, success=result)


if __name__ == "__main__":
    app()
