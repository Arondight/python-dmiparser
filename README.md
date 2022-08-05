# python-dmiparser

## About

This parse dmidecode output to JSON.

## Installation

```shell
pip3 install -U dmiparser
```

## Usage

### Use dmiparser directly

```python
#!/usr/bin/env python3
import json
from dmiparser import DmiParser


if "__main__" == __name__:
    from functools import partial
    from typing import Callable, Any


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


    text = (
        "# dmidecode 3.0\n"
        "Getting SMBIOS data from sysfs.\n"
        "SMBIOS 2.7 present.\n"
        "\n"
        "Handle 0x0003, DMI type 2, 17 bytes\n"
        "Base Board Information\n"
        "\tManufacturer: Intel Corporation\n"
        "\tProduct Name: S2600WT2R\n"
        "\tVersion: H21573-372\n"
        "\tSerial Number: BQWL81150522\n"
        "\tAsset Tag: Base Board Asset Tag\n"
        "\tFeatures:\n"
        "\t\tBoard is a hosting board\n"
        "\t\tBoard is replaceable\n"
        "\tLocation In Chassis: Part Component\n"
        "\tChassis Handle: 0x0000\n"
        "\tType: Motherboard\n"
        "\tContained Object Handles: 0\n"
        "\n"
    )

    # parser = DmiParser(text)
    parser = DmiParser(text, sort_keys=True, indent=2)

    parsedStr = str(parser)  # get str
    parsedObj = json.loads(str(parser))  # get object

    reportSecs(parsedStr, parsedObj)
```

### Use the default wrapper

```python
from dmiparser.wrapper import DmiDecode


if "__main__" == __name__:
    from functools import partial
    from typing import Callable, Any


    def getCpuInfo(dmidecode) -> str:
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

        for id, name in dmidecode.sections:
            def getFirst(*args):
                vals = dmidecode.getProp(*args, id=id, name=name)
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


    dmidecode4 = DmiDecode("-t 4", sort_keys=True, indent=2)  # Type 4 is Processor

    reportSecs(dmidecode4.text, str(dmidecode4.data), getCpuInfo(dmidecode4))
```

### Get full JSON text using an executable

```shell
dmiparser
```

> Tip: Superuser permissions are required here to run `dmidecode`.

## Development

### Test

```shell
tox
```

## License

[MIT LICENSE](https://github.com/Arondight/python-dmiparser/blob/master/LICENSE).
