"""水躍：超臨界流轉為亞臨界流。Bélanger 共軛水深與能量損失。

    y2 / y1 = (sqrt(1 + 8 Fr1^2) - 1) / 2         （矩形斷面）
    ΔE = (y2 - y1)^3 / (4 y1 y2)
"""
import math

from channelwatch.config import BED_WIDTH
from channelwatch.hydraulics import froude


def conjugate_depth(q: float, y1: float, b: float = BED_WIDTH) -> float:
    """下游共軛水深 [m]。"""
    fr1 = froude(q, y1, b)
    return y1 / 2 * (math.sqrt(1 + 8 * fr1) - 1)


def energy_loss(y1: float, y2: float) -> float:
    return (y2 - y1) ** 3 / (4 * y1 * y2)
