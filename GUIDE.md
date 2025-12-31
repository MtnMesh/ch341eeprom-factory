# Step by Step EEPROM Programming Guide

## First time setup

1. Install pre-requisite packages

    #### Debian / Ubuntu

    ```shell
    apt update
    apt install git make clang libusb-1.0-0-dev
    ```

    #### Fedora
    ```shell
    dnf update
    dnf install git make clang libusb1-devel
    ```

2. Clone, Compile, and Install `ch341eeprom` utility
    ```shell
    git clone https://github.com/command-tab/ch341eeprom.git
    cd ch341eeprom
    make
    sudo install -m755 ch341eeprom /usr/local/bin/
    ```

3. Test that `ch341eeprom` utility is working
    ```shell
    ch341eeprom --help
    ```
    Should return basic version / usage information.

4. Clone the programming script `ch341eeprom-factory`
    ```shell
    git clone https://github.com/MtnMesh/ch341eeprom-factory.git
    cd ch341eeprom-factory
    ```

## Programming

All programming steps will be completed within the `ch341eeprom-factory` directory.

1. Initiate programming

    You must specify the *starting* serial number.
    ```shell
    python3 ch341_factory.py --serial 13374201 --product MESHTOAD --major-version 1 --minor-version 0
    ```
    This example programs a device as MESHTOAD Hardware Version `1.0`, serial number `13374201`.

    Ensure that you are holding the `Program` button when plugging in the device, or ch341eeprom will fail to read/write.

2. Ensure success

    > Programmed EEPROM for MESHTOAD 13374201
    >
    > New EEPROM Contents: ...

    If programming successful, a message similar to this will be displayed.

3. Repeat

    After programming, the script will continue to run in a loop, adding +1 to the serial number and keeping all other values the same.
    Ex: 13374201, 13374202, 13374203, etc

## Errors (FAQ)

> Couldn't open device [1a86:5512]
>
> Couldnt configure USB device with vendor ID: 1a86 product ID: 5512

A CH341 device in *programming mode* cannot be found.

Ensure that you are holding the `Program` button when plugging in the device, and try again.
