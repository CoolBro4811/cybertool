from cybertool.hookspecs import hookspec


@hookspec
def config_modify(config: dict) -> dict:
    config["PermitRootLogin"] = "no"
    config["PasswordAuthentication"] = "no"
    return config


@hookspec
def after_apply(target: str, success: bool) -> None:
    print(f"[ssh_hardening] Hardened SSH config at {target}")
