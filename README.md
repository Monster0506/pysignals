# signals

Small reactive primitives for Python: **signal**, **computed**, and **effect**. Dependencies are tracked automatically. **`computed`** reuses its last result until a dependency changes, then recomputes on the next read. **`effect`** re-runs when anything it read updates.

## Requirements

Python 3.12+

## Install

```bash
uv sync
```

Or install the package in editable mode:

```bash
pip install -e .
```

## Usage

```python
from signals import signal, computed, effect

count = signal[int](0)
doubled = computed[int](lambda: count.value * 2)

effect(lambda: print(f"count={count.value}, doubled={doubled.value}"))

count.value += 1
```

## Demo

```bash
python main.py
```
