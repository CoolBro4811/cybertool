from .hookspecs import hookspec


@hookspec
def config_modify(config: dict) -> dict:
    # Example: add a marker
    config["# managed_by"] = "cybertool"
    return config


@hookspec
def after_apply(target: str, success: bool) -> None:
    print(f"[example_plugin] Config applied to {target}: success={success}")
