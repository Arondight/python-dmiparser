from dmiparser.dmiparser import DmiParser

__version__ = "5.1"
__all__ = ["DmiParser", "main"]


def main() -> None:
    from sys import stdin
    from argparse import ArgumentParser

    parser = ArgumentParser(description="This parse dmidecode output to JSON text")
    parser.add_argument("-f", "--format", action="store_true", required=False, help="format JSON text")
    args = parser.parse_args()
    fmtOpts = {"sort_keys": True, "indent": 2}
    dmiparser = DmiParser(stdin.read(), **(fmtOpts if args.format is True else {}))

    print(str(dmiparser))
