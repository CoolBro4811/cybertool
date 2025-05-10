import logging
import subprocess


def setup_logger(level=logging.INFO):
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=level
    )


def validate_ssh_config(path: str) -> bool:
    """Run `sshd -t -f <path>` to test syntax."""
    try:
        subprocess.run(["sshd", "-t", "-f", path], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
