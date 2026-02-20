"""
Bibliomantic divination (enhanced-only).

This module re-exports the enhanced divination implementation so that
existing code using "from divination import BiblioManticDiviner, ..."
continues to work. All divination now uses the traditional three-coin
method with changing lines and secondary hexagram (see enhanced_divination.py).
"""

from typing import Tuple

try:
    from .enhanced_divination import (
        EnhancedBiblioManticDiviner,
        augment_query_with_divination,
        perform_divination,
    )
except ImportError:
    from enhanced_divination import (
        EnhancedBiblioManticDiviner,
        augment_query_with_divination,
        perform_divination,
    )

# Backward compatibility: old code expects BiblioManticDiviner class
BiblioManticDiviner = EnhancedBiblioManticDiviner

__all__ = [
    "BiblioManticDiviner",
    "augment_query_with_divination",
    "perform_divination",
]
