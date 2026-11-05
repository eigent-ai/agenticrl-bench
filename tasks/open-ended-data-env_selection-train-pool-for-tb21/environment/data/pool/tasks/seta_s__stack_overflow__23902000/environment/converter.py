"""Binary sensor data reader and fixed-point converter."""

import struct


def read_sdb(filepath):
    """Read an SDB1 binary file and return raw int16 samples.

    Returns:
        tuple: (channel_count, sample_count, raw_data)
            raw_data is a list of lists, each inner list has channel_count int16 values
    """
    with open(filepath, 'rb') as f:
        magic = f.read(4)
        if magic != b'SDB1':
            raise ValueError(f"Invalid file format: expected SDB1 magic, got {magic!r}")

        channel_count = struct.unpack('<H', f.read(2))[0]
        sample_count = struct.unpack('<I', f.read(4))[0]

        raw_data = []
        for _ in range(sample_count):
            row = []
            for _ in range(channel_count):
                val = struct.unpack('<h', f.read(2))[0]
                row.append(val)
            raw_data.append(row)

    return channel_count, sample_count, raw_data


def convert_to_float(raw_data):
    """Convert raw int16 fixed-point values to floating point.

    The int16 values represent fixed-point numbers that need to be
    scaled to their actual floating-point representation.
    """
    result = []
    for row in raw_data:
        converted = []
        for val in row:
            fval = val / 16383.0
            fval = max(-1.0, min(1.0, fval))
            converted.append(fval)
        result.append(converted)
    return result
