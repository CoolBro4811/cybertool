from cybertool.hookspecs import hookimpl, hookspec


@hookspec
@hookimpl
def config_modify(config: dict) -> dict:
    # Example, adding a marker
    config["# managed_by"] = "cybertool"
    return config


@hookspec
@hookimpl
def before_apply(target: str) -> bool:
    # This can be used to create backups, etc...
    print(f"Running before_apply on {target}")
    return True


@hookspec
@hookimpl
def after_apply(target: str, success: bool) -> None:
    # This can be used to restart processes (systemctl, etc)...
    print(f"[example_plugin] Config applied to {target}: success={success}")
