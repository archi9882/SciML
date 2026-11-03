"""排程：失敗時自動重試。"""


def run_with_retry(fn, retries: int = 100):
    """執行 fn()；任何例外都立刻重試，最多 retries 次。"""
    last = None
    for _ in range(retries):
        try:
            return fn()
        except Exception as e:
            last = e
    raise last
