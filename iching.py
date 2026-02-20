"""
I Ching interface (enhanced-only).

This module re-exports the enhanced I Ching implementation so that
existing code using "from iching import IChing, divine_hexagram" continues
to work. All divination now uses the traditional three-coin method with
changing lines and secondary hexagram (see enhanced_iching_core.py).
"""

from typing import Tuple

try:
    from .enhanced_iching_core import IChingAdapter, EnhancedIChing
except ImportError:
    from enhanced_iching_core import IChingAdapter, EnhancedIChing

# Backward compatibility: old code expects IChing class
IChing = IChingAdapter


def divine_hexagram() -> Tuple[int, str, str]:
    """Generate a hexagram using the enhanced three-coin method (with changing lines)."""
    _iching = IChingAdapter()
    return _iching.generate_hexagram_by_coins()


if __name__ == "__main__":
    print("I Ching (enhanced) – three-coin method with changing lines")
    print("=" * 50)
    iching = IChingAdapter()
    for i in range(3):
        number, name, interpretation = iching.generate_hexagram_by_coins()
        print(f"\nDivination {i+1}: {number} - {name}")
        print(interpretation)
