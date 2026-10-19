"""The book's figures, hand-laid out with dg.py and chartkit.py. Run build.py to write _includes/diagrams/.

Every figure is its own module in figs/ (fig_<chapter>_<n>.py), which registers itself with @figure.
"""
import importlib
import os
import pkgutil

from registry import FIGURES  # noqa: F401  (re-exported for build.py)

_figs = os.path.join(os.path.dirname(__file__), "figs")
for _m in sorted(pkgutil.iter_modules([_figs]), key=lambda m: m.name):
    importlib.import_module(f"figs.{_m.name}")
