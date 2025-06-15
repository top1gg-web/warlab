import argparse, importlib, sys
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser(prog="warlab")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # register available modules here
    for name in ("wifi", "scout"):
        sub.add_parser(name)

    args = parser.parse_args()
    mod = importlib.import_module(f"warlab.modules.{args.cmd}")
    mod.cli_entry(args)

if __name__ == "__main__":
    main()
