import json
from dmiparser import DmiParser
from pathlib import Path

RDIR = Path(Path(__file__).resolve()).parents[0]


def test_dmidecode_10() -> None:
    count = 0
    on_board_device = 0

    with open(RDIR / "dmidecode_10.txt", "rt") as f:
        text = f.read()
        data = json.loads(str(DmiParser(text)))

    for d in data:
        """
        Handle 0x005F, DMI type 10, 20 bytes
        On Board Device 1 Information
                Type: Video
                Status: Enabled
                Description: ServerEngines Pilot III
        On Board Device 2 Information
                Type: Ethernet
                Status: Enabled
                Description: Intel I350
        """
        if "0x005F" == d["handle"]["id"]:
            on_board_device += 1

    assert 8 == on_board_device
    count += 1

    assert 1 == count
