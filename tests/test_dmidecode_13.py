import json
from pathlib import Path
from dmiparser import DmiParser

RDIR = Path(Path(__file__).resolve()).parents[0]

def test_dmidecode_13():
    text = open(RDIR / 'dmidecode_13.txt', 'rt').read()
    data = json.loads(str(DmiParser(text)))
    testnum = 0

    for d in data:
        '''
        Installable Languages: 1
                enUS
        '''
        if '0x000C' == d['handle']['id'] and 'BIOS Language Information' == d['name']:
            assert(2 == len(d['props']['Installable Languages']['values']))
            testnum += 1

    assert(1 == testnum)

