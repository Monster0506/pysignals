from typing import Callable

from .shared import ComputeContext, stack


class computed[T]:
    def __init__(self, fn: Callable[[], T]):
        self.dirty: bool = True
        self.cachedValue: T = fn.__call__()
        self.fn = fn
        self.subs: set[ComputeContext] = set()
        self.sources: set[Callable[[], None]] = set()

    def _recompute(self):
        for source in self.sources:
            source.__call__()
        self.sources.clear()

        def set_dirty(_: T | None = None) -> None:
            if self.dirty:
                return
            self.dirty = True
            for sub in list(self.subs):
                sub.setDirty()

        stack.append(ComputeContext(set_dirty, lambda x: self.sources.add(x)))

        self.cachedValue = self.fn.__call__()
        dirty = False
        stack.pop()

    @property
    def value(self) -> T:
        return self.cachedValue

    @value.getter
    def value(self) -> T:
        if len(stack) > 0 and (currentComputed := stack[-1]):
            currentComputed = stack[-1]
            self.subs.add(currentComputed)
            currentComputed.addSource(lambda: self.subs.remove(currentComputed))

        if self.dirty:
            self._recompute()
        return self.cachedValue
