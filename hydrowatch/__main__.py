"""命令列入口：python -m hydrowatch run | api"""
import argparse
import json

from hydrowatch import pipeline
from hydrowatch.api.app import serve


def main() -> int:
    p = argparse.ArgumentParser(prog="hydrowatch")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("run", help="執行整條流程，輸出到 outputs/")
    sub.add_parser("api", help="啟動 REST API（port 8000）")
    a = p.parse_args()

    if a.cmd == "run":
        report = pipeline.run()
        print(json.dumps(report["runoff"], indent=2))
        print("已輸出到 outputs/")
    else:
        serve()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
