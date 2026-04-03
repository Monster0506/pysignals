from typing import Callable

from .shared import stack


class signal[T]:
    def __init__(self, val: T):
        self.subscribers: set[Callable[[T], None]] = set()
        self._value: T = val

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, new_value: T):
        self._value = new_value
        for subscriber in list(self.subscribers):
            subscriber.__call__(self.value)

    @value.getter
    def value(self) -> T:
        if len(stack) > 0 and (currentComputed := stack[-1]):
            self.subscribers.add(currentComputed.setDirty)
            currentComputed.addSource(
                lambda: self.subscribers.remove(currentComputed.setDirty)
            )
        return self._value

    def subscribe(self, fn: Callable[[T], None]):
        self.subscribers.add(fn)
