# python-dmiparser

## About

This parse dmidecode output to JSON.

## Installation

```shell
pip3 install -U dmiparser
```

## Usage

```python
#!/usr/bin/env python3
import json
from dmiparser import DmiParser

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

    parser = DmiParser(text)
    # parser = DmiParser(text, sort_keys=True, indent=2)

    # get string
    print(str(parser))

    # get object
    print(json.loads(str(parser)))
```

## Example

Here is a simple [example](https://github.com/Arondight/python-dmiparser/blob/master/examples/dmidecode.py) to show how to use dmiparser.

## License

[MIT LICENSE](https://github.com/Arondight/python-dmiparser/blob/master/LICENSE).
