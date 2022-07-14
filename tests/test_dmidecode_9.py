import json
from pathlib import Path
from dmiparser import DmiParser

RDIR = Path(Path(__file__).resolve()).parents[0]


def test_dmidecode_9():
    testnum = 0

    with open(RDIR / "dmidecode_9.txt", "rt") as f:
        text = f.read()
        data = json.loads(str(DmiParser(text)))

    for d in data:
        """
        Bus Address: 0000:00:03.2
        """
        if "0x0007" == d["handle"]["id"] and "System Slot Information" == d["name"]:
            assert "0000:00:03.2" == d["props"]["Bus Address"]["values"][0]
            testnum += 1

    assert 1 == testnum
