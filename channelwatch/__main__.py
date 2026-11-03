"""命令列入口：python -m channelwatch run"""
import json

from channelwatch import pipeline

if __name__ == "__main__":
    print(json.dumps(pipeline.run(), indent=2))
