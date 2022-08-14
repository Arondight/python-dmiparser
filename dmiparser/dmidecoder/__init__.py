from dmiparser.dmidecoder.dmidecoder import DmiDecoder

__all__ = ["DmiDecoder", "main"]


def main() -> None:
    from argparse import ArgumentParser

    parser = ArgumentParser(description="This is a simple dmiparser dmidecoder")
    parser.add_argument("-f", "--format", action="store_true", required=False, help="format JSON text")
    parser.add_argument(
        "-a", "--arguments", nargs=1, type=str, required=False, help="arguments passed to dmidecode command"
    )
    args = parser.parse_args()
    fmtOpts = {"sort_keys": True, "indent": 2}
    dmidecoder = DmiDecoder(
        args.arguments[0] if isinstance(args.arguments, list) and len(args.arguments) > 0 else None,
        **(fmtOpts if args.format is True else {})
    )

    print(dmidecoder.text)
