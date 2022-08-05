from dmiparser.dmiparser import DmiParser

__version__ = "4.0"
__all__ = ["DmiParser"]


def main() -> None:
    from sys import stdin

    print(str(DmiParser(stdin.read(), sort_keys=True, indent=2)))


if "__main__" == __name__:
    main()
