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


if "__main__" == __name__:
    from functools import partial
    from typing import Callable, Any


    def getCpuInfo(dmidecoder) -> str:
        """Get CPU information, will return text like below.

        CPU1:
            Family: Xeon
            Version: Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz
            Voltage: 1.8 V
            Speed: 2200 MHz/4000 MHz
            Status: Populated, Enabled
            Core: 10/10
            Thread: 20
        CPU2:
            Family: Xeon
            Version: Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz
            Voltage: 1.8 V
            Speed: 2200 MHz/4000 MHz
            Status: Populated, Enabled
            Core: 10/10
            Thread: 20

        @param: dmidecode: DmiDecode object
        @return: text of CPU information
        """
        text = ""

        for id, name in dmidecoder.sections:
            def getFirst(*args):
                vals = dmidecoder.getProp(*args, id=id, name=name)
                return vals[0] if len(vals) > 0 else None

            text += "{}:\n".format(getFirst("Socket Designation"))
            text += "\tFamily: {}\n".format(getFirst("Family"))
            text += "\tVersion: {}\n".format(getFirst("Version"))
            text += "\tVoltage: {}\n".format(getFirst("Voltage"))
            text += "\tSpeed: {}/{}\n".format(getFirst("Current Speed"), getFirst("Max Speed"))
            text += "\tStatus: {}\n".format(getFirst("Status"))
            text += "\tCore: {}/{}\n".format(getFirst("Core Enabled"), getFirst("Core Count"))
            text += "\tThread: {}\n".format(getFirst("Thread Count"))

        return text


    def reportSecs(*args: str, brWidth=80) -> None:
        """report texts format by section

        @param args: text string
        @param brWidth: br width
        """
        br: Callable[[Any], None] = lambda c: print("-" * c)
        brn = partial(br, brWidth)

        brn()

        for text in args:
            print(text)
            brn()


    dmidecoder4 = DmiDecoder("-t 4", sort_keys=True, indent=2)  # Type 4 is Processor

    reportSecs(dmidecoder4.text, str(dmidecoder4.data), getCpuInfo(dmidecoder4))
