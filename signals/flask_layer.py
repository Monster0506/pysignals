"""Thin Flask + Jinja glue for signals.

Jinja evaluates filters and expressions synchronously during ``render_template``.
If a template uses ``{{ n | unwrap }}`` or ``{{ n.value }}``, those reads run at
render time.

Dependency tracking only records reads that occur while the reactive stack is
active — i.e. while rendering runs *inside* a ``computed`` or ``effect`` body
(same thread, before that frame returns). A normal Flask route that calls
``render_template`` without that wrapper still evaluates the template, but
**no** subscriptions are recorded, so nothing re-runs when signals change later.
"""

from __future__ import annotations

from typing import Any

from flask import Flask


def unwrap(v: Any) -> Any:
    """Return ``v.value`` when the object has that attribute, else ``v``."""
    if hasattr(v, "value"):
        return v.value
    return v


def register_jinja_helpers(app: Flask) -> None:
    """Register the ``unwrap`` Jinja filter on ``app``."""
    app.template_filter("unwrap")(unwrap)
