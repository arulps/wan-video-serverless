import argparse
import json
import sys


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("path", help="dot path, e.g. template.name")
    ap.add_argument("--default", default=None)
    ap.add_argument("--raw-json", action="store_true")
    args = ap.parse_args()

    data = json.load(open(args.file, encoding="utf-8"))
    for part in args.path.split("."):
        if args.default is not None and data in ({}, None):
            print(args.default)
            return
        try:
            if isinstance(data, list):
                data = data[int(part)]
            else:
                data = data[part]
        except (KeyError, IndexError, TypeError, ValueError):
            if args.default is not None:
                print(args.default)
                return
            print("", file=sys.stderr)
            sys.exit(1)

    if data is None:
        print(args.default if args.default is not None else "")
        return
    if isinstance(data, (dict, list)) or args.raw_json:
        print(json.dumps(data, separators=(",", ":")))
    elif isinstance(data, bool):
        print("true" if data else "false")
    else:
        print(data)


if __name__ == "__main__":
    main()