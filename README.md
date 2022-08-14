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

### Python 3 script

#### DmiParser

This accepts a `str` (with the output of `dmidecode`) as argument and converts it to JSON text.

```python
#!/usr/bin/env python3
import json
from dmiparser import DmiParser
from functools import partial


def report(*args: str) -> None:
    """report texts with format

    @param args: text string
    """
    br = lambda e: print("-" * e)
    brn = partial(br, 80)

    brn()

    for e in args:
        print(e)
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

    report(parsedStr, parsedObj)
```

#### DmiDecoder (the default wrapper)

This run `dmidecode` and converting the output of the command to JSON text.

```python
from dmiparser.dmidecoder import DmiDecoder
from functools import partial


def report(*args: str) -> None:
    """report texts with format

    @param args: text string
    """
    br = lambda e: print("-" * e)
    brn = partial(br, 80)

    brn()

    for e in args:
        print(e)
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

    report(dmidecoder4.text, str(dmidecoder4.data), getCpuInfo(dmidecoder4))
```

> Tip: Superuser permissions are required here to run `dmidecode`.

### Executable command

#### dmiparser

This read output of `dmidecode` from pipe and print it as JSON text.

```shell
sudo dmidecode | dmiparser
sudo dmidecode -t 4 | dmiparser --format
```

```shell
sudo dmidecode >/tmp/dmidecode.txt
dmiparser </tmp/dmidecode.txt
```

> Tip: you can run `dmiparser` module as a script (use `python3 -m dmiparser` instead of `dmiparser` command).

#### dmidecoder

This run `dmidecode` and print the output as JSON text.

```shell
sudo dmidecoder
sudo dmidecoder --arguments "-t 4" --format
```

> Tip: you can run `dmiparser.dmidecoder` module as a script (use `python3 -m dmiparser.dmidecoder` instead
> of `dmidecoder` command).

## Development

### Test

```shell
tox
```

### Format

```shell
black -l 120 ./dmiparser/ ./tests/
```

## License

[MIT LICENSE](https://github.com/Arondight/python-dmiparser/blob/master/LICENSE).
