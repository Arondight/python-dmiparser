import json
from subprocess import check_output

from dmiparser import DmiParser

__all__ = ["DmiDecoder"]


class DmiDecoder(object):
    """This is a simple dmiparser wrapper"""

    def __init__(self, arguments: str = None, command: str = "dmidecode", **kwargs) -> None:
        """
        @param arguments: command's extra arguments like "-t 4"
        @param command: an executable dmidecode command
        @param kwargs: these will pass to dmiparser
        """
        self._command = command

        if arguments:
            self._command = "{} {}".format(self._command, arguments)

        try:
            text = check_output(self._command, shell=True, encoding="utf8")
            parser = DmiParser(text, **kwargs)
            self._text = str(parser)
            self._data = json.loads(self._text)
        except Exception:
            # XXX do something here
            raise

    @property
    def text(self) -> str:
        """
        @return: dmidecode output parsed JSON text
        """
        return self._text

    @property
    def data(self) -> list:
        """
        @return: dmidecode output parsed JSON object
        """
        return self._data

    @property
    def sections(self) -> list:
        """
        @return: a list for all section id and section name
        """
        return [(x["handle"]["id"], x["name"]) for x in self.data]

    def get(self, *keys: str, id: str = "", name: str = "") -> list:
        """get information for a section

        @param keys: hash keys for a section
        @param id: section id like '0x0020'
        @param name: section name like 'Processor Information'
        @return: section information values
        """
        if len(keys) == 0:
            raise AttributeError("{}.{} does not accept empty keys".format(self.__class__, self.get.__name__))

        data = self._data
        values = []

        for d in data:
            if id and id != d["handle"]["id"]:
                continue

            if name and name != d["name"]:
                continue

            d_ = d

            for k in keys:
                try:
                    d_ = d_[k]
                except (KeyError, TypeError):
                    d_ = None
                    break

            if d_:
                values.extend(d_)

        return values

    def getProp(self, prop: str, id: str = None, name: str = None) -> list:
        """get values for a section property

        @param prop: property name
        @param id: section id like '0x0020'
        @param name: section name like 'Processor Information'
        @return: section property values
        """
        keys = ["props"]
        keys.extend([prop, "values"])

        return self.get(*keys, id=id, name=name)
