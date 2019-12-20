import json
from pathlib import Path
from dmiparser import DmiParser

RDIR = Path(Path(__file__).resolve()).parents[0]

def test_dmidecode_full():
    text = open(RDIR / 'dmidecode_full.txt', 'rt').read()
    data = json.loads(str(DmiParser(text)))
    testnum = 0

    '''
    Handle 0xFEFF, DMI type 127, 4 bytes
        End Of Table
    '''
    assert(111 == len(data))
    testnum += 1

    assert(1 == testnum)

