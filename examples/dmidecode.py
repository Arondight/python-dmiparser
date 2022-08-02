#!/usr/bin/env python3
import json
from subprocess import check_output
from typing import Any, Callable, Union

from dmiparser import DmiParser

__all__ = ["DmiDecode"]


class DmiDecode(object):
    """This is a simple example to show how to use dmiparser"""

    def __init__(self, arguments: str = None, command: str = "dmidecode") -> None:
        """
        @param arguments: command's extra arguments like "-t 4"
        @param command: a executable dmidecode command
        """
        self._command = command

        if arguments:
            self._command = "{} {}".format(self._command, arguments)

        try:
            text = check_output(self._command, shell=True, encoding="utf8")
            parser = DmiParser(text)
            self._text = str(parser)
            self._data = json.loads(self._text)
        except Exception:
            # XXX do something here
            raise

    def text(self) -> str:
        return self._text

    def data(self) -> list[Any]:
        return self._data

    def sections(self) -> list[Union[Any, Any]]:
        return [(x["handle"]["id"], x["name"]) for x in self._data]

    def get(self, *keys: str, id: str = "", name: str = "") -> list[str]:
        """get information for a section

        @param keys: hash keys for a section
        @param id: section id like '0x0020'
        @param name: section name like 'Processor Information'
        """
        if len(keys) == 0:
            raise AttributeError("{}.{} does not accept empty parameters".format(self.__class__, self.get.__name__))

        data = self._data
        values: list[str] = []

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

    def getProp(self, prop: str, id: str = None, name: str = None) -> list[str]:
        """get values for a section property

        @param prop: property name
        @param id: section id like '0x0020'
        @param name: section name like 'Processor Information'
        """
        keys_ = ["props"]
        keys_.extend([prop, "values"])

        return self.get(*keys_, id=id, name=name)


if "__main__" == __name__:
    """Show CPU information, will print output like below.

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
    """
    from functools import partial

    dmi = DmiDecode("-t 4")  # Type 4 is Processor
    secs = dmi.sections()

    for id, name in secs:
        getVals = partial(dmi.getProp, id=id, name=name)
        # XXX Here assumes that all items exist
        getFirst: Callable[[Any], Any] = lambda *args: getVals(*args)[0]

        print("{}:".format(getFirst("Socket Designation")))

        print("\tFamily: {}".format(getFirst("Family")))
        print("\tVersion: {}".format(getFirst("Version")))
        print("\tVoltage: {}".format(getFirst("Voltage")))
        print("\tSpeed: {}/{}".format(getFirst("Current Speed"), getFirst("Max Speed")))
        print("\tStatus: {}".format(getFirst("Status")))
        print("\tCore: {}/{}".format(getFirst("Core Enabled"), getFirst("Core Count")))
        print("\tThread: {}".format(getFirst("Thread Count")))
