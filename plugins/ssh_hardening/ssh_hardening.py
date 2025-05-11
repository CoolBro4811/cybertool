import os
import shutil

import yaml

from cybertool.hookspecs import hookimpl, hookspec
from cybertool.utils import (
    backup_file,
    detect_os_key,
    make_backup_dir,
    run_command,
    validate_ssh_config,
)

GUIDE_DIR = os.path.join(os.path.dirname(__file__), "guides")
OS_KEY = None
GUIDE = {}


def load_guide() -> dict:
    p = os.path.join(GUIDES_DIR, f"{OS_KEY}.yaml")
    if not os.path.exists(p):
        return {}
    with open(p) as f:
        return yaml.safe_load(f)


@hookspec
@hookimpl
def config_modify(config: dict) -> dict:
    config["PermitRootLogin"] = "no"
    config["MaxAuthTries"] = 3
    config["LoginGraceTime"] = 20
    config["PermitEmptyPasswords"] = "no"
    config["ChallengeResponseAuthentication"] = "no"
    config["KerberosAuthentication"] = "no"
    config["GSSAPIAuthentication"] = "no"
    config["X11Forwarding"] = "no"
    config["PermitUserEnvironment"] = "no"
    config["AllowAgentForwarding"] = "no"
    config["AllowTcpForwarding"] = "no"
    config["PermitTunnel"] = "no"
    config["DebianBanner"] = "no"
    config["PasswordAuthentication"] = "no"

    for cmd in GUIDE.get("config_modify", []):
        print(f"[ssh_hardening] config_modify: {cmd}")
        run_command(cmd)

    return config


@hookspec
@hookimpl
def before_apply(target: str) -> bool:
    print(f"Running before_apply on {target}")

    backup_dir = make_backup_dir("ssh_hardening")
    backup_file(target, backup_dir)
    backup_file("/etc/ssh/ssh_host_ed25519_key", backup_dir)
    backup_file("/etc/ssh/ssh_host_rsa_key", backup_dir)
    backup_file("/etc/ssh/moduli", backup_dir)
    backup_file("/etc/ssh/sshd_config.d/ssh-audit_hardening.conf", backup_dir)
    backup_file("/etc/ssh/sshd_config", backup_dir)

    OS_KEY = detect_os_key()
    GUIDE = load_guide()

    for cmd in GUIDE.get("before_apply", []):
        print(f"[ssh_hardening] before-apply: {cmd}")
        run_command(cmd)

    print(f"[ssh_hardening] backups -> {backup_dir}")

    return True


@hookspec
@hookimpl
def after_apply(target: str, success: bool) -> None:
    if not success:
        print(f"[ssh_hardening] !!! FAILED at {target}!")
        return
    validate_ssh_config(target)
    run_command("sudo systemctl reload sshd.service")

    for audit in GUIDE.get("after_apply", []):
        print(f"[ssh_hardening] after_apply: {audit}")
        run_command(audit)

    cmd = GUIDE.get("reload_command")
    if not cmd:
        cmd = (
            "sudo systemctl reload sshd"
            if os.name == "posix"
            else "powershell Start-Service sshd –Force"
        )
    print(f"[ssh_hardening] reload: {cmd}")
    run_command(cmd)

    print(
        f"[ssh_hardening] Done hardening and reloading SSH. Config file at: {target}"
    )
