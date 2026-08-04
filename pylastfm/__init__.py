"""pylastfm — Last.fm artist catalog bulk harvester, grouped on harvestkit.

Importing this package imports :mod:`pylastfm.harvest`, which in turn
imports the scraper module so it registers itself with
:mod:`harvestkit.engine` (``@register``).
"""
from pylastfm.version import __version__

import pylastfm.harvest  # noqa: F401  (import for @register side effects)

__all__ = ["__version__"]
