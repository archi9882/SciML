"""明渠水力：斷面幾何、Manning 正常水深、臨界水深、Froude 數。

    Q = (1/n) A R^(2/3) S^(1/2)        A：斷面積，R = A / P：水力半徑，P：濕周
"""
import math

from channelwatch.config import BED_SLOPE, BED_WIDTH, G, MANNING_N, SIDE_SLOPE


def area(y: float, b: float = BED_WIDTH, z: float = SIDE_SLOPE) -> float:
    return (b + z * y) * y


def wetted_perimeter(y: float, b: float = BED_WIDTH, z: float = SIDE_SLOPE) -> float:
    return b + 2 * y * math.sqrt(1 + z * z)


def top_width(y: float, b: float = BED_WIDTH, z: float = SIDE_SLOPE) -> float:
    return b + 2 * z * y


def manning_q(y: float, n: float = MANNING_N, s0: float = BED_SLOPE, b: float = BED_WIDTH,
              z: float = SIDE_SLOPE) -> float:
    """水深 y 時的 Manning 流量 [m3/s]。"""
    a = area(y, b, z)
    r = a / wetted_perimeter(y, b, z)
    return 1.486 / n * a * r ** (2 / 3) * math.sqrt(s0)


def normal_depth(q: float, n: float = MANNING_N, s0: float = BED_SLOPE, b: float = BED_WIDTH,
                 z: float = SIDE_SLOPE) -> float:
    """正常水深 [m]：寬淺渠道近似 R ≈ y，q = Q/B = (1/n) y^(5/3) S^(1/2)。"""
    qu = q / b
    return (qu * n / math.sqrt(s0)) ** 0.6


def froude(q: float, y: float, b: float = BED_WIDTH, z: float = SIDE_SLOPE) -> float:
    v = q / area(y, b, z)
    return v / math.sqrt(G * y)


def critical_depth(q: float, b: float = BED_WIDTH) -> float:
    """臨界水深 [m]：yc = (q^2 / g)^(1/3)，q 為單寬流量。"""
    return ((q / b) ** 2 / G) ** (1 / 3)


def specific_energy(q: float, y: float, b: float = BED_WIDTH, z: float = SIDE_SLOPE) -> float:
    v = q / area(y, b, z)
    return y + v * v / (2 * G)
