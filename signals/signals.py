from typing import Callable

from .shared import stack

Notify = Callable[..., None]


class signal[T]:
    __slots__ = ("subscribers", "_value")

    def __init__(self, val: T):
        self.subscribers: set[Notify] = set()
        self._value: T = val

    @property
    def value(self) -> T:
        if stack and (ctx := stack[-1]):
            self.subscribers.add(ctx.setDirty)
            ctx.addSource(lambda: self.subscribers.discard(ctx.setDirty))
        return self._value

    @value.setter
    def value(self, new_value: T):
        self._value = new_value
        for subscriber in list(self.subscribers):
            subscriber.__call__(self.value)

    def subscribe(self, fn: Callable[[T], None]) -> None:
        self.subscribers.add(fn)
