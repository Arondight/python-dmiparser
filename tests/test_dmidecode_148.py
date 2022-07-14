import json
from pathlib import Path
from dmiparser import DmiParser

RDIR = Path(Path(__file__).resolve()).parents[0]


def test_dmidecode_148():
    testnum = 0

    with open(RDIR / "dmidecode_148.txt", "rt") as f:
        text = f.read()
        data = json.loads(str(DmiParser(text)))

    for d in data:
        """
        Strings:
                SE5C610.86B.01.01.0022.062820171903
                 1.80.10802
                3.1.3.43
        """
        if "0x0066" == d["handle"]["id"] and "OEM-specific Type" == d["name"]:
            assert 35 == len(d["props"]["Strings"]["values"])
            testnum += 1

    assert 1 == testnum
