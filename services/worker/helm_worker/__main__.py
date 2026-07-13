import argparse
import asyncio
import json
from collections.abc import Sequence

from helm_worker.health import health_payload


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="helm-worker")
    parser.add_argument("command", choices=("health", "run"))
    args = parser.parse_args(argv)

    if args.command == "health":
        print(json.dumps(health_payload(), sort_keys=True))
    if args.command == "run":
        print(json.dumps({**health_payload(), "state": "idle"}, sort_keys=True), flush=True)
        try:
            asyncio.run(asyncio.Event().wait())
        except KeyboardInterrupt:
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
