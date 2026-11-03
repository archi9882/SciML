"""漸變流水面線：標準步推法（standard step method）。

由控制斷面的已知水深，沿河道逐段求出下一個斷面的水深，使能量方程式平衡：
    y1 + V1^2/2g + S0 dx = y2 + V2^2/2g + Sf dx          （由下游往上游推）
"""
import math

from channelwatch.config import BED_SLOPE, BED_WIDTH, G, MANNING_N, SIDE_SLOPE
from channelwatch.hydraulics import area, wetted_perimeter


def friction_slope(q: float, y: float, n: float = MANNING_N) -> float:
    a = area(y)
    r = a / wetted_perimeter(y)
    return (n * q / (a * r ** (2 / 3))) ** 2


def standard_step(q: float, y_control: float, length: float, dx: float = 100.0,
                  n: float = MANNING_N) -> list[tuple[float, float]]:
    """從下游控制斷面往上游推，回傳 [(距控制斷面的距離 [m], 水深 [m]), ...]。"""
    out = [(0.0, y_control)]
    y = y_control
    x = 0.0
    while x < length:
        v1 = q / area(y)
        e1 = y + v1 * v1 / (2 * G)
        # 上游斷面的水深，用一次修正求得
        y2 = y
        sf = friction_slope(q, y, n)
        e2 = e1 + (sf - BED_SLOPE) * dx
        for _ in range(1):
            y2 = y + (e2 - e1)
        x += dx
        y = max(y2, 0.05)
        out.append((x, y))
    return out
