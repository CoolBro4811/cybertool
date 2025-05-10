import pluggy

HOOK_NAMESPACE = "cybertool"
hookspec = pluggy.HookspecMarker(HOOK_NAMESPACE)


class Spec:
    @hookspec
    def config_modify(self, config: dict) -> dict:
        """Modify the parsed config dict and return it."""

    @hookspec
    def before_apply(self, target: str) -> None:
        """Called before applying any changes."""

    @hookspec
    def after_apply(self, target: str, success: bool) -> None:
        """Called after applying changes."""
