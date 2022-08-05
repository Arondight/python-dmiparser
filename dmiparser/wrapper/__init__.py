from dmiparser.wrapper.dmidecoder import DmiDecoder

__all__ = ["DmiDecoder"]


def main() -> None:
    from argparse import ArgumentParser

    parser = ArgumentParser(description="This parse dmidecode output to JSON text")
    parser.add_argument("-f", "--format", action="store_true", required=False, help="format JSON text")
    args = parser.parse_args()
    print(DmiDecoder(**({"sort_keys": True, "indent": 2} if args.format is True else {})).text)


if "__main__" == __name__:
    main()
