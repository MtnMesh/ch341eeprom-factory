import os
import subprocess
import argparse

class eepCH341(object):
    """
    :param size_str: EEPROM size string      - default "24c02"
    :param size_bytes: EEPROM size in bytes  - default 256
    :param majorVersion: Major version number
    :param minorVersion: Minor version number
    :param serial: Serial number (8 bytes)
    :param product: Product string (up to 95 bytes)
    :param MODE: Mode byte            - default 0x12
    :param CFG: Configuration byte    - default 0xCC
    :param VID: Vendor ID (2 bytes)   - default (0x1A, 0x86)
    :param PID: Product ID (2 bytes)  - default (0x55, 0x12)
    """

    def __init__(
            self, majorVersion: bytes, minorVersion: bytes, serial: str, product: str,
            size_str: str = "24c02", size_bytes: int = 256,
            MODE: bytes = 0x12, CFG: bytes = 0xCC, VID: bytearray = (0x1A, 0x86), PID: bytearray = (0x55, 0x12)
    ):
        self.size = size_str
        self.size_bytes = size_bytes
        self.majorVersion = majorVersion
        self.minorVersion = minorVersion
        if len(serial) == 8:
            self.serial = serial
        else:
            raise ValueError("Serial number must be 8 digits")
        if len(product) < 95:
            self.product = product
        else:
            raise ValueError("Product string too long, max 95 characters")
        self.MODE = MODE
        self.CFG = CFG
        self.VID = VID
        self.PID = PID

    def __str__(self):
        return f"EEPROM: {self.majorVersion}.{self.minorVersion} {self.serial} {self.product}"
    
    def bytes(self):
        """
        Generate the EEPROM bytes
        :return: bytearray of EEPROM
        """
        rom = bytearray(self.size_bytes-1)
        rom[0] = 0x53
        rom[1] = self.MODE
        rom[2] = self.CFG
        rom[3] = 0x00
        rom[4] = self.VID[1]
        rom[5] = self.VID[0]
        rom[6] = self.PID[1]
        rom[7] = self.PID[0]
        rom[8] = self.minorVersion
        rom[9] = self.majorVersion
        # Bytes 10-15 are padding
        # Serial number (bytes 16-23)
        serial_bytes = bytearray(self.serial.encode('ascii'))
        rom[16:23] = serial_bytes
        # Bytes 24-31 are padding
        # Product String bytes (32-127)
        product_bytes = bytearray(self.product.encode('ascii'))
        rom[32:32 + len(product_bytes)] = product_bytes
        return rom

    def hex(self):
        return self.bytes().hex()

    def erase(self, bin_ch341eeprom: str):
        r = subprocess.run([
            bin_ch341eeprom,
            # "--verbose",
            "--erase",
            "--size", self.size
        ], check=True)
        return r

    def read(self, bin_ch341eeprom: str):
        # Delete existing read_eeprom.bin file if it exists
        if os.path.exists("read_eeprom.bin"):
            os.remove("read_eeprom.bin")
        # Use `ch341eeprom` to read the EEPROM
        r = subprocess.run([
            bin_ch341eeprom,
            # "--verbose",
            "--read", "read_eeprom.bin",
            "--size", self.size
        ], capture_output=True, check=True)

        # Read the EEPROM file and return it as a byte array
        with open("read_eeprom.bin", "rb") as f:
            data = f.read()
        os.remove("read_eeprom.bin")

        return data

    def flash(self, bin_ch341eeprom: str):
        # Delete existing write_eeprom.bin file if it exists
        if os.path.exists("write_eeprom.bin"):
            os.remove("write_eeprom.bin")
        # Write the byte array to a temp file
        with open("write_eeprom.bin", "wb") as f:
            f.write(self.bytes())
        # Use `ch341eeprom` to flash the EEPROM
        r = subprocess.run([
            bin_ch341eeprom,
            # "--verbose",
            "--write", "write_eeprom.bin",
            "--size", self.size
        ], check=True)
        os.remove("write_eeprom.bin")

        return r
    
    def verify(self, bin_ch341eeprom: str):
        # Delete existing verify_eeprom.bin file if it exists
        if os.path.exists("verify_eeprom.bin"):
            os.remove("verify_eeprom.bin")
        # Write the byte array to a temp file
        with open("verify_eeprom.bin", "wb") as f:
            f.write(self.bytes())
        # Use `ch341eeprom` to verify the EEPROM
        r = subprocess.run([
            bin_ch341eeprom,
            # "--verbose",
            "--verify", "verify_eeprom.bin",
            "--size", self.size
        ], check=True)
        os.remove("verify_eeprom.bin")

        return r

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CH341 EEPROM programmer utility")
    parser.add_argument("--serial", type=int, default=13374204,
                        help="8-digit serial number (default: 13374201)")
    parser.add_argument("--product", default="MESHTOAD",
                        help="Product name (default: MESHTOAD)")
    parser.add_argument("--major-version", type=int, default=1, dest="majorVersion",
                        help="Major version number (default: 1)")
    parser.add_argument("--minor-version", type=int, default=2, dest="minorVersion",
                        help="Minor version number (default: 2)")
    parser.add_argument("--bin", default="/home/vidplace7/Documents/GitHub/ch341eeprom/ch341eeprom", 
                        help="Path to ch341eeprom binary (default: /home/vidplace7/Documents/GitHub/ch341eeprom/ch341eeprom)")
    args = parser.parse_args()

    cur_serial = int(args.serial)

    while True:
        input(f"Attach serial number: {cur_serial}")
        eeprom = eepCH341(args.majorVersion, args.minorVersion, str(cur_serial), args.product)
        # print(eeprom.hex())

        # Read the EEPROM before flashing
        read_init = eeprom.read(args.bin)
        if len(read_init) != eeprom.size_bytes:
            raise ValueError(f"EEPROM read error: expected {eeprom.size_bytes} bytes, got {len(read_init)} bytes")

        # Erase the EEPROM
        eeprom.erase(args.bin)

        # Flash/verify the EEPROM
        eeprom.flash(args.bin)
        eeprom.verify(args.bin)
        print(f"Flashed EEPROM for {args.product} {cur_serial}")

        # Read the EEPROM again
        read_again = eeprom.read(args.bin)
        print("New EEPROM Contents:")
        # Print the first 128 bytes of the EEPROM
        print(read_again[0:127])
        print("")

        cur_serial += 1
