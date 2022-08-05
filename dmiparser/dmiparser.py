import json
import re
from enum import Enum, auto
from itertools import takewhile
from typing import Union

__all__ = ["DmiParser"]


class DmiParserState(Enum):
    NONE = auto()
    GET_SECT = auto()
    GET_PROP = auto()
    GET_PROP_ITEM = auto()


class DmiParserSectionHandle(object):
    """A handle looks like this

    Handle 0x0066, DMI type 148, 48 bytes
    """

    def __init__(self) -> None:
        self.id = ""
        self.type = ""
        self.bytes = 0

    def __str__(self) -> str:
        """
        @return: JSON dump string
        """
        return json.dumps(self.__dict__)


class DmiParserSectionProp(object):
    """A property looks like this

    Characteristics:
            3.3 V is provided
            PME signal is supported
            SMBus signal is supported
    """

    def __init__(self, value: str) -> None:
        """
        @param value: property text
        """
        self.values = []

        if value:
            self.append(value)

    def __str__(self) -> str:
        """
        @return: JSON dump string
        """
        return json.dumps(self.__dict__)

    def append(self, item: str) -> None:
        """
        @param item: item value
        """
        self.values.append(item)


class DmiParserSection(object):
    """A section looks like this

    On Board Device 1 Information
            Type: Video
            Status: Enabled
            Description: ServerEngines Pilot III
    """

    def __init__(self) -> None:
        self.handle = None
        self.name = ""
        self.props = {}

    def __str__(self) -> str:
        """
        @return: JSON dump string
        """
        return json.dumps(self.__dict__)

    def append(self, key: str, prop: str) -> None:
        """
        @param key: property name
        @param prop: property
        """
        self.props[key] = prop


class DmiParser(object):
    """This parse dmidecode output to JSON text"""

    def __init__(self, text: str, **kwargs) -> None:
        """
        @param text: output of command dmidecode
        @param kwargs: these will pass to json.dumps()
        """
        if type(text) is not str:
            raise TypeError("{} want a {} but got {}".format(self.__class__, type(__name__), type(text)))

        self._text = text
        self._kwargs = kwargs
        self._indentLv = lambda l: len(list(takewhile(lambda c: "\t" == c, l)))
        self._sections = []

        self._parse()

    def __str__(self) -> str:
        """
        @return: JSON dump string
        """
        return json.dumps(self._sections, **self._kwargs)

    def _parse(self) -> None:
        state: DmiParserState = DmiParserState.NONE
        handle: Union[DmiParserSectionHandle, None] = None
        prop: Union[DmiParserSectionProp, None] = None
        section: Union[DmiParserSection, None] = None
        k: Union[str, None] = None
        lines = self._text.splitlines()

        for i, line in enumerate(lines):
            if i == len(lines) - 1 or DmiParserState.GET_SECT == state:
                # Add previous section if exist
                if section:
                    # Add previous prop if exist
                    if prop:
                        section.append(k, json.loads(str(prop)))
                        prop = None

                    self._sections.append(json.loads(str(section)))
                    section = None

            if not line:
                continue

            if line.startswith("Handle"):
                regex = r"^Handle\s(.+?),\sDMI\stype\s(\d+?),\s(\d+?)\sbytes$"
                state = DmiParserState.GET_SECT
                handle = DmiParserSectionHandle()
                match = re.match(regex, line)
                handle.id, handle.type, handle.bytes = match.groups()
                continue

            if DmiParserState.GET_SECT == state:
                section = DmiParserSection()
                section.handle = json.loads(str(handle))
                section.name = line
                state = DmiParserState.GET_PROP
                continue

            lv = self._indentLv(line)

            if i < len(lines) - 1:
                lv -= self._indentLv(lines[i + 1])

            if DmiParserState.GET_PROP == state:
                k, v = [x.strip() for x in line.split(":", 1)]
                prop = DmiParserSectionProp(v)

                if v:
                    if -1 == lv:
                        state = DmiParserState.GET_PROP_ITEM
                        continue

                    if 0 == lv:
                        section.append(k, json.loads(str(prop)))
                        prop = None
                else:
                    if -1 == lv:
                        state = DmiParserState.GET_PROP_ITEM
                        continue

                # Next section for this handle
                if i < len(lines) - 1:
                    if 0 == self._indentLv(lines[i + 1]):
                        state = DmiParserState.GET_SECT

            if DmiParserState.GET_PROP_ITEM == state:
                prop.append(line.strip())

                if 0 != lv:
                    section.append(k, json.loads(str(prop)))
                    prop = None
                    state = DmiParserState.GET_SECT if lv > 1 else DmiParserState.GET_PROP
