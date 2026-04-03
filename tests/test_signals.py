from signals import computed, effect, signal


def test_computed_tracks_dependencies_from_construction():
    n = signal[int](1)
    doubled = computed[int](lambda: n.value * 2)
    assert doubled.value == 2
    n.value = 5
    assert doubled.value == 10


def test_computed_does_not_recompute_when_clean():
    n = signal[int](0)
    calls = 0

    def fn() -> int:
        nonlocal calls
        calls += 1
        return n.value * 2

    d = computed[int](fn)
    assert calls == 1
    _ = d.value
    assert calls == 1
    _ = d.value
    assert calls == 1
    n.value = 1
    _ = d.value
    assert calls == 2


def test_effect_reruns_when_dependency_changes():
    s = signal[int](0)
    seen: list[int] = []
    effect(lambda: seen.append(s.value))
    assert seen == [0]
    s.value = 1
    assert seen == [0, 1]


def test_subscribe_receives_updates():
    s = signal[int](0)
    log: list[int] = []
    s.subscribe(log.append)
    s.value = 3
    assert log == [3]
