# python-dmiparser

## ABOUT

This parse dmidecode output to JSON.

## USAGE

```python
#!/usr/bin/env python3
import json
from dmiparser import DmiParser

if '__main__' == __name__:
    text='''# dmidecode 3.0
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

    '''

    # just print
    parser = DmiParser(text)
    #parser = DmiParser(text, sort_keys=True, indent=2)
    print("parser is %s" %(type(parser)))
    print(parser)

    # if you want a string
    dmistr = str(parser)
    print("dmistr is %s" %(type(dmistr)))
    print(dmistr)

    # if you want a data structure
    dmidata = json.loads(str(parser))
    print("dmidata is %s" %(type(dmidata)))
    print(dmidata)
```

## EXAMPLE

Here is an simple [example](examples/dmidecode.py) to show how to use dmiparser.

## COPYRIGHT

Copyright (c) 2019 Qin Fandong

## LICENSE

Read [LICENSE](LICENSE).

