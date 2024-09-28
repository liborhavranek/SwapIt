from flask import template_rendered
from contextlib import contextmanager

@contextmanager
def captured_templates(app):
    """Context manager to capture templates used during a request."""
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append(template)

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)