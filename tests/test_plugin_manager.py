from pathlib import Path

from cybertool.manager import PluginManager


class DummyPlugin:
    def config_modify(self, config):
        config["test_key"] = "test_value"
        return config

    def before_apply(self, target):
        print(f"Running before_apply on {target}")

    def after_apply(self, target, success):
        print(f"Running after_apply on {target} with success={success}")


def test_plugin_hook_executes(tmp_path):
    manager = PluginManager(plugin_paths=[])

    # Register dummy manually
    manager.pm.register(DummyPlugin())

    config = {"original": "keep"}
    results = manager.run_hook("config_modify", config)
    assert results[0]["test_key"] == "test_value"

    # Ensure before/after hooks do not raise
    manager.run_hook("before_apply", str(tmp_path / "test"))
    manager.run_hook("after_apply", str(tmp_path / "test"), True)
