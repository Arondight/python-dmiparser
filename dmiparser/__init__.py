import re
import json
from itertools import takewhile
from enum import Enum

__version__ = '0.1'

DmiParserState = Enum (
    'DmiParserState',
    (
        'GET_SECTS',
        'GET_PROPS',
        'GET_PROP_ITEMS',
    )
)

class DmiParserSectionHandle(object):
    def __init__(self):
        self.id= ''
        self.type = ''
        self.bytes = 0

    def __str__(self):
        return json.dumps(self.__dict__)

class DmiParserSectionProps(object):
    def __init__(self, value):
        self.values = []

        if value:
            self.append(value)

    def __str__(self):
        return json.dumps(self.__dict__)

    def append(self, item):
        self.values.append(str(item))

class DmiParserSection(object):
    def __init__(self):
        self.handle = None
        self.name = ''
        self.props = {}

    def __str__(self):
        return json.dumps(self.__dict__)

    def append(self, key, prop):
        self.props[key] = prop

class DmiParser(object):
    def __init__(self, text, **kwargs):
        self._text = text
        self._kwargs = kwargs
        self._indentLv = lambda l: len(list(takewhile(lambda c: "\t" == c, l)))
        self._sections = []
        self._parse(text)

    def __str__(self):
        return json.dumps(self._sections, **self._kwargs)

    def _parse(self, text):
        lines = self._text.splitlines()
        rhandle = r'^Handle\s(.+?),\sDMI\stype\s(\d+?),\s(\d+?)\sbytes$'
        section = None
        prop = None
        state = None

        for i, l in enumerate(lines):
            if i == len(lines) - 1:
                self._sections.append(json.loads(str(section)))
                section = None

            if not l:
                continue

            if l.startswith('Handle'):
                state = DmiParserState.GET_SECTS
                handle = DmiParserSectionHandle()
                match = re.match(rhandle, l)
                handle.id, handle.type, handle.bytes = match.groups()
                continue

            if DmiParserState.GET_SECTS == state:
                # Add previous section
                if section:
                    # Add previous prop
                    if prop:
                        section.append(k, json.loads(str(prop)))
                        prop = None

                    self._sections.append(json.loads(str(section)))
                    section = None

                section = DmiParserSection()
                section.handle = json.loads(str(handle))
                section.name = l
                state = DmiParserState.GET_PROPS
                continue

            if DmiParserState.GET_PROPS == state:
                k, v = [x.strip() for x in l.split(':', 1)]
                prop = DmiParserSectionProps(v)
                lv = self._indentLv(l) - self._indentLv(lines[i+1])

                if v:
                    if not lv:
                        section.append(k, json.loads(str(prop)))
                        prop = None
                    elif -1 == lv:
                        state = DmiParserState.GET_PROP_ITEMS
                        continue
                else:
                    if -1 == lv:
                        state = DmiParserState.GET_PROP_ITEMS
                        continue

                # Next section for this handle
                if not self._indentLv(lines[i+1]):
                    state = DmiParserState.GET_SECTS

            if DmiParserState.GET_PROP_ITEMS == state:
                prop.append(l.strip())

                lv = self._indentLv(l) - self._indentLv(lines[i+1])

                if lv:
                    section.append(k, json.loads(str(prop)))
                    prop = None

                    if lv > 1:
                        state = DmiParserState.GET_SECTS
                    else:
                        state = DmiParserState.GET_PROPS

if '__main__' == __name__:
    text='''# dmidecode 3.0
Getting SMBIOS data from sysfs.
SMBIOS 2.7 present.

Handle 0x0003, DMI type 2, 17 bytes
Base Board Information
	Manufacturer: Intel Corporation
	Product Name: S2600WT2R
	Version: H21573-372
	Serial Number: BQWL81150522
	Asset Tag: Base Board Asset Tag
	Features:
		Board is a hosting board
		Board is replaceable
	Location In Chassis: Part Component
	Chassis Handle: 0x0000
	Type: Motherboard
	Contained Object Handles: 0

    '''

    # just print
    parser = DmiParser(text)
    #parser = DmiParser(text, sort_keys=True, indent=2)
    print("parser is %s" %(type(parser)))
    print(parser)

    # if you want a string
    dmistr = str(parser)
    print("dmistr is %s" %(type(dmistr)))
    print(dmistr)

    # if you want a data structure
    dmidata = json.loads(str(parser))
    print("dmidata is %s" %(type(dmidata)))
    print(dmidata)

