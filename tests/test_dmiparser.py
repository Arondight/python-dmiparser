import json
from pathlib import Path
from dmiparser import DmiParser

RDIR = Path(Path(__file__).resolve()).parents[0]

def test_full_dmidecode_output():
    text = open(RDIR / 'dmidecode_full.txt', 'rt').read()
    data = json.loads(str(DmiParser(text)))
    on_board_device = 0
    testnum = 0

    '''
    Handle 0xFEFF, DMI type 127, 4 bytes
        End Of Table
    '''
    assert(111 == len(data))
    testnum += 1

    for d in data:
        '''
        Strings:
                SE5C610.86B.01.01.0022.062820171903
                 1.80.10802
                3.1.3.43
        '''
        if '0x0066' == d['handle']['id'] and 'OEM-specific Type' == d['name']:
            assert(35 == len(d['props']['Strings']['values']))
            testnum += 1

        '''
        Installable Languages: 1
                enUS
        '''
        if '0x000C' == d['handle']['id'] and 'BIOS Language Information' == d['name']:
            assert(2 == len(d['props']['Installable Languages']['values']))
            testnum += 1

        '''
        Bus Address: 0000:00:03.2
        '''
        if '0x0007' == d['handle']['id'] and 'System Slot Information' == d['name']:
            assert('0000:00:03.2' == d['props']['Bus Address']['values'][0])
            testnum += 1

        if '0x005F' == d['handle']['id']:
            on_board_device += 1

    '''
    Handle 0x005F, DMI type 10, 20 bytes
    On Board Device 1 Information
            Type: Video
            Status: Enabled
            Description: ServerEngines Pilot III
    On Board Device 2 Information
            Type: Ethernet
            Status: Enabled
            Description: Intel I350
    '''
    assert(8 == on_board_device)
    testnum += 1

    assert(5 == testnum)

