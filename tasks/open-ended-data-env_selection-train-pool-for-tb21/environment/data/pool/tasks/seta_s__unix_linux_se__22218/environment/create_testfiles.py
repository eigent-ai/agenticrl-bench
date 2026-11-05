import os

files = {
    '/srv/testfiles/small.txt':       100,
    '/srv/testfiles/with spaces.txt': 500,
    '/srv/testfiles/medium.txt':      1000,
    '/srv/testfiles/large.txt':       9000,
    '/srv/testfiles/-':               10000,
}

for path, size in files.items():
    with open(path, 'w') as f:
        f.write('a' * size)
