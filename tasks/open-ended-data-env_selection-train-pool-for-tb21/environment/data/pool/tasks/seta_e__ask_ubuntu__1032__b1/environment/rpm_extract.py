#!/usr/bin/python3
"""
Extract the cpio payload from an RPM file.
Usage: python3 rpm_extract.py <file.rpm>
Writes the raw (compressed) payload to stdout.
This is equivalent to rpm2cpio but without depending on librpm/libcurl.
"""
import sys
import struct

def rpm2cpio(filename):
    with open(filename, 'rb') as f:
        data = f.read()

    # RPM lead is 96 bytes
    offset = 96

    # Parse signature header section
    magic = struct.unpack('>I', data[offset:offset+4])[0]
    if magic != 0x8eade801:
        raise ValueError(f"Bad signature header magic: {hex(magic)}")
    nindex = struct.unpack('>I', data[offset+8:offset+12])[0]
    hsize = struct.unpack('>I', data[offset+12:offset+16])[0]
    offset += 16 + nindex * 16 + hsize
    # Align to 8-byte boundary
    offset = (offset + 7) & ~7

    # Parse main header section
    magic = struct.unpack('>I', data[offset:offset+4])[0]
    if magic != 0x8eade801:
        raise ValueError(f"Bad main header magic: {hex(magic)}")
    nindex = struct.unpack('>I', data[offset+8:offset+12])[0]
    hsize = struct.unpack('>I', data[offset+12:offset+16])[0]
    offset += 16 + nindex * 16 + hsize

    # The rest is the compressed cpio payload
    sys.stdout.buffer.write(data[offset:])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.rpm>", file=sys.stderr)
        sys.exit(1)
    rpm2cpio(sys.argv[1])
