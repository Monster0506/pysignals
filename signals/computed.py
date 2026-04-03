from typing import Callable

from .shared import ComputeContext, stack


class computed[T]:
    def __init__(self, fn: Callable[[], T]):
        self.fn = fn
        self.subs: set[ComputeContext] = set()
        self.sources: set[Callable[[], None]] = set()
        self.dirty = True
        self.cachedValue = self._execute()

    def _execute(self) -> T:
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
        try:
            result = self.fn.__call__()
        except BaseException:
            self.dirty = True
            raise
        finally:
            stack.pop()

        self.dirty = False
        return result

    @property
    def value(self) -> T:
        if stack and (ctx := stack[-1]):
            self.subs.add(ctx)
            ctx.addSource(lambda: self.subs.remove(ctx))

        if self.dirty:
            self.cachedValue = self._execute()
        return self.cachedValue
