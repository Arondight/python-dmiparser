# python-dmiparser

## About

This parse `dmidecode` output to JSON text.

## Installation

### PyPI

```shell
pip3 install -U dmiparser
```

### RPM

```shell
git clone https://github.com/Arondight/python-dmiparser.git
cd ./python-dmiparser/
python3 ./setup.py bdist --format=rpm
sudo dnf install ./dist/dmiparser-*.noarch.rpm
```

> Tip: Requires the `rpm-build` package in your Linux distribution.

## Usage

### Python3 script

#### DmiParser

This accepts a `str` (with the output of `dmidecode`) as argument and converts it to JSON text.

```python
#!/usr/bin/env python3
import json
from dmiparser import DmiParser
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


if "__main__" == __name__:
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

#### DmiDecoder (the default wrapper)

This runs `dmidecode` and converting the output of the command to JSON text.

```python
from dmiparser.wrapper import DmiDecoder
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


if "__main__" == __name__:
    # dmidecoder = DmiDecoder()
    dmidecoder4 = DmiDecoder("-t 4", sort_keys=True, indent=2)  # Type 4 is Processor

    reportSecs(dmidecoder4.text, str(dmidecoder4.data), getCpuInfo(dmidecoder4))
```

> Tip: Superuser permissions are required here to run `dmidecode`.

### Executable command

#### dmiparser

This read output of `dmidecode` from pipe and converts it to JSON text.

```shell
sudo dmidecode | dmiparser
sudo dmidecode -t 4 | dmiparser
```

```shell
sudo dmidecode >/tmp/dmidecode.txt
dmiparser </tmp/dmidecode.txt
```

### dmidecoder

This run `dmidecode` and converts **full** output to JSON text.

```shell
sudo dmidecoder
sudo dmidecoder --format
```

## Development

### Test

```shell
tox
```

## License

[MIT LICENSE](https://github.com/Arondight/python-dmiparser/blob/master/LICENSE).
