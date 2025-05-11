from cybertool.hookspecs import hookimpl, hookspec
from cybertool.manager import PluginManager


class DummyPlugin:
    @hookspec
    @hookimpl
    def config_modify(self, config: dict) -> dict:
        config["test_key"] = "test_value"
        return config

    @hookspec
    @hookimpl
    def before_apply(self, target) -> bool:
        print(f"Running before_apply on {target}")
        return True

    @hookspec
    @hookimpl
    def after_apply(self, target, success) -> None:
        print(f"Running after_apply on {target} with success={success}")


def test_plugin_hook_executes(tmp_path: str):
    manager = PluginManager(plugin_paths=[])

    manager.pm.register(DummyPlugin())

    cfg = {"original": "keep"}
    results = manager.run_hook("config_modify", config=cfg)
    print(results)
    assert len(results[0].keys()) > 0, "Values in cfg are not saved/removed"
    assert results[0]["test_key"] == "test_value"

    result = manager.run_hook("before_apply", target=str(tmp_path / "test"))
    assert result[0] is True, "before_apply failed"
    manager.run_hook(
        "after_apply", target=str(tmp_path / "test"), success=result
    )
