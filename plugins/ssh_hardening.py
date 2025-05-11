from cybertool.hookspecs import hookimpl, hookspec


@hookspec
@hookimpl
def config_modify(config: dict) -> dict:
    config["PermitRootLogin"] = "no"
    config["PasswordAuthentication"] = "yes"
    return config


@hookspec
@hookimpl
def before_apply(target: str) -> bool:
    print(f"Running before_apply on {target}")
    return True


@hookspec
@hookimpl
def after_apply(target: str, success: bool) -> None:
    if not success:
        print(f"[ssh_hardening] SSH Hardening Failed at {target}!")
        return
    print(f"[ssh_hardening] Hardened SSH config at {target}")
