import json
from pathlib import Path
from dmiparser import DmiParser

RDIR = Path(Path(__file__).resolve()).parents[0]

def test_dmidecode_32():
    text = open(RDIR / 'dmidecode_32.txt', 'rt').read()
    data = json.loads(str(DmiParser(text)))
    testnum = 0

    for d in data:
        '''
        System Boot Information
            Status: No errors detected
        '''
        if '0x000F' == d['handle']['id'] and 'System Boot Information' == d['name']:
            assert('No errors detected' == d['props']['Status']['values'][0])
            testnum += 1

    assert(1 == testnum)

