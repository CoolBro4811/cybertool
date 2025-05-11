import datetime
import logging
import os
import shutil
import subprocess


def setup_logger(level=logging.INFO):
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=level
    )


def validate_ssh_config(path: str) -> bool:
    """Run `sshd -t -f <path>` to test syntax (verifying tests)"""
    try:
        subprocess.run(["sshd", "-t", "-f", path], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def run_command(command: str) -> bool:
    try:
        subprocess.run(command.split(), check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def make_backup_dir(plugin: str):
    ts = datetime.datetime.now().strftime("__%Y%m%d_%H%M%S")
    backup_dir = os.path.join(f"/var/backups/{plugin}", ts)
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def backup_file(path: str, backup_dir: str):
    if os.path.exists(path):
        shutil.copy2(path, backup_dir)


def detect_os_key():
    data = {}
    with open("/etc/os-release") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                data[k] = v.strip('"')
    name = data.get("ID", "").lower()
    version = data.get("VERSION_ID", "").strip('"')
    if name.startswith("linuxmint"):
        version = "22.04" if version.startswith("21") else version
        name = "ubuntu"
    return f"{name}_{version}"
