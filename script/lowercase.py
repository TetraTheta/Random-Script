import os
import sys
from pathlib import Path


class Color:
    CYAN = "\033[0;36m"
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    RESET = "\033[0m"
    YELLOW = "\033[1;33m"


def lowercase(dir: Path):
    items = sorted(Path(dir).rglob("*"), key=lambda p: len(p.parts), reverse=True)
    for item in items:
        new_name = item.name.lower()
        if item.name != new_name:
            new_path = item.with_name(new_name)
            print(f"{Color.YELLOW}RENAME{Color.RESET} {item.parent}{os.sep}{{{Color.YELLOW}{item.name}{Color.RESET} → {Color.YELLOW}{new_name}{Color.RESET}}}")
            item.rename(new_path)


if __name__ == "__main__":
    # Parse command line
    from argparse import ArgumentParser

    cli = ArgumentParser(prog="lowercase", description="Convert uppercase characters to lowercase in name of file or directory")
    cli.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")
    cli.add_argument("target", type=Path, default=Path.cwd().resolve(), nargs="?", help="Target directory")

    args = cli.parse_args()

    args.target = args.target.resolve()

    if not args.target.is_dir():
        print(f"{Color.RED}ERROR{Color.RESET} Given path '{args.target}' is not a directory")
        sys.exit(1)

    if not args.yes:
        print(f"{Color.GREEN}TARGET{Color.RESET} {args.target}")
        result = input("Do you want to lowercase any sub directory or files of this directory? (yes/no): ")
        if result.lower() == "yes" or result.lower() == "y":
            lowercase(args.target)
        else:
            print(f"{Color.RED}ERROR{Color.RESET} User canceled the opration")
            sys.exit(1)
    else:
        lowercase(args.target)
