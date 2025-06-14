#!/usr/bin/env python3
import argparse
from modules import wifi, scout

def main():
    p = argparse.ArgumentParser(prog="warlab")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("wifi").set_defaults(func=wifi.cli_entry)
    sub.add_parser("scout").set_defaults(func=scout.cli_entry)
    args = p.parse_args(); args.func(args)

if __name__ == "__main__":
    main()
