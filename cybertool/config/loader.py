import os
import shutil
import tempfile

from jinja2 import Environment, FileSystemLoader
from ruamel.yaml import YAML

yaml = YAML()


def load_template(path: str, context: dict) -> dict:
    env = Environment(loader=FileSystemLoader(os.path.dirname(path)))
    tpl = env.get_template(os.path.basename(path))
    rendered = tpl.render(**context)
    return yaml.load(rendered)


def write_atomic(path: str, data: dict):
    dirpath = os.path.dirname(path)
    tmp = tempfile.NamedTemporaryFile(delete=False, dir=dirpath)
    yaml.dump(data, tmp)
    tmp.flush()
    tmp.close()
    shutil.move(tmp.name, path)
