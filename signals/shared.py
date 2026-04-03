from typing import Callable, Protocol
from types import SimpleNamespace
class ComputeContext:
    def __init__(self, set_dirty: Callable[[], None], add_source: Callable[[Callable[[], None]], None]):
        self.setDirty = set_dirty
        self.addSource = add_source



stack: list[ComputeContext] = []