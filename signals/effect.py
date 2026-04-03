from typing import Callable

from .shared import ComputeContext, stack


class effect:
    def __init__(self, fn: Callable[[], None]):
        self.fn = fn
        self.sources: set[Callable[[], None]] = set()
        self._run()

    def _run(self):
        for source in self.sources:
            source.__call__()
        self.sources.clear()

        def set_dirty(_=None):
            self._run()

        stack.append(ComputeContext(set_dirty, lambda x: self.sources.add(x)))
        self.fn.__call__()
        stack.pop()
