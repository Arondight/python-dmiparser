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
    text = """# dmidecode 3.0
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

    """

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
