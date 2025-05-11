import importlib
from pathlib import Path

import pluggy

from cybertool.hookspecs import HOOK_NAMESPACE, Spec


class PluginManager:
    def __init__(self, plugin_paths: list[Path]):
        self.pm = pluggy.PluginManager(HOOK_NAMESPACE)
        self.pm.add_hookspecs(Spec)
        self._load_plugins(plugin_paths)

    def _load_plugins(self, paths):
        print(paths)
        for p in paths:
            if p.is_dir():
                for py_file in p.glob("**/*.py"):
                    self._load_plugin_file(py_file)
            elif p.is_file() and p.suffix == ".py":
                self._load_plugin_file(p)

    def _load_plugin_file(self, py_file: Path):
        try:
            print(py_file.stem)
            spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "hookspec"):
                self.pm.register(module)
        except Exception as e:
            print(f"Failed to load plugin {py_file.stem}: {e}")

    def run_hook(self, hook_name: str, **kwargs):
        return getattr(self.pm.hook, hook_name)(**kwargs)
