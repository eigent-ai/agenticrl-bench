import ctypes
import os
import sys

def load_processor():
    lib_path = "/app/lib/libprocessor.so"
    try:
        lib = ctypes.CDLL(lib_path)
        return lib
    except OSError as e:
        print(f"Error loading shared library: {e}", file=sys.stderr)
        raise

def process_matrix(data):
    lib = load_processor()
    n = len(data)
    arr_type = ctypes.c_double * (n * n)
    c_data = arr_type(*[item for row in data for item in row])
    lib.process_data(c_data, ctypes.c_int(n))
    result = [[c_data[i*n + j] for j in range(n)] for i in range(n)]
    return result
