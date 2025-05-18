# ch341eeprom-factory
Flash system EEPROM for CH341A / CH341F in small batches.

Intended for use with [MeshToad](https://oshwlab.com/mtnmesh/meshtoad-v1-2), [MeshStick](https://github.com/markbirss/MESHSTICK), [MikroToad](https://oshwlab.com/nomdetom/meshtoad-v1-2_copy) and their cousins.


## Prerequisites

- [command-tab/ch341eeprom](https://github.com/command-tab/ch341eeprom)
  - `ch341eeprom` must be compiled with `make` and added to the `$PATH` or specified with `--bin`


## Usage
```
usage: ch341_factory.py [-h] [--serial SERIAL] [--product PRODUCT] [--major-version MAJORVERSION] [--minor-version MINORVERSION] [--bin BIN]

CH341 EEPROM programmer utility

options:
  -h, --help            show this help message and exit
  --serial SERIAL       8-digit serial number (default: 13374201)
  --product PRODUCT     Product name (default: MESHTOAD)
  --major-version MAJORVERSION
                        Major version number (default: 1)
  --minor-version MINORVERSION
                        Minor version number (default: 2)
  --bin BIN             Path to ch341eeprom binary (default: ch341eeprom from PATH)
```

The script will loop through serial numbers beginning with the number specified in `--serial`.
