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
        "	Manufacturer: Intel Corporation\n"
        "	Product Name: S2600WT2R\n"
        "	Version: H21573-372\n"
        "	Serial Number: BQWL81150522\n"
        "	Asset Tag: Base Board Asset Tag\n"
        "	Features:\n"
        "		Board is a hosting board\n"
        "		Board is replaceable\n"
        "	Location In Chassis: Part Component\n"
        "	Chassis Handle: 0x0000\n"
        "	Type: Motherboard\n"
        "	Contained Object Handles: 0\n"
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
