import json
from dmiparser import DmiParser
from pathlib import Path

RDIR = Path(Path(__file__).resolve()).parents[0]


def test_dmidecode_13() -> None:
    count = 0

    with open(RDIR / "dmidecode_13.txt", "rt") as f:
        text = f.read()
        data = json.loads(str(DmiParser(text)))

    for d in data:
        """
        Installable Languages: 1
                enUS
        """
        if "0x000C" == d["handle"]["id"] and "BIOS Language Information" == d["name"]:
            assert 2 == len(d["props"]["Installable Languages"]["values"])
            count += 1

    assert 1 == count
