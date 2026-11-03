"""transport.f90 的 Python 翻譯版（由 AI 翻譯）。"""
import numpy as np

N, NSTEPS = 100, 400
L, D, U, DT = 10.0, 0.5, 0.68, 0.0096


def main() -> None:
    dx = L / N
    x = (np.arange(N) + 0.5) * dx
    c = np.exp(-((x - 8.0) / 0.5) ** 2)

    for _ in range(NSTEPS):
        cn = np.zeros(N)
        cn[0] = 0.0                                   # 上游端：擾動固定為 0
        for i in range(2, N - 1):
            cn[i] = (c[i] - U * DT * (c[i] - c[i - 1]) / dx
                     + D * DT * (c[i + 1] - 2.0 * c[i] + c[i - 1]) / dx ** 2)
        cn[N - 1] = c[N - 1]                          # 下游端：零梯度（自由流出）
        c = cn

    print(f"peak = {c.max():10.6f}")
    print(f"sum  = {c.sum():10.6f}")


if __name__ == "__main__":
    main()
