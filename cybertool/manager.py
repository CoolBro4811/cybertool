from pathlib import Path

import pluggy

from .hookspecs import HOOK_NAMESPACE, Spec


class PluginManager:
    def __init__(self, plugin_paths: list[Path]):
        self.pm = pluggy.PluginManager(HOOK_NAMESPACE)
        self.pm.add_hookspecs(Spec)
        self._load_plugins(plugin_paths)

    def _load_plugins(self, paths):
        for p in paths:
            try:
                if p.suffix == ".py":
                    spec = pluggy.util.spec_from_file_location(p.stem, p)
                    module = pluggy.util.module_from_spec(spec)
                    spec.loader.exec_module(module)  # type: ignore
                    self.pm.register(module)
            except Exception as e:
                print(f"⚠️  Failed to load plugin {p.stem}: {e}")

    def run_hook(self, hook_name: str, *args, **kwargs):
        return getattr(self.pm.hook, hook_name)(*args, **kwargs)
