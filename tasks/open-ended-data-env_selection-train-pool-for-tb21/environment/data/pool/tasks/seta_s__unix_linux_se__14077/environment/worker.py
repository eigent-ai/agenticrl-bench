#!/usr/bin/env python3
import time
import os

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def main():
    pid = os.getpid()
    num = 2
    while True:
        batch = 0
        while batch < 5000:
            is_prime(num)
            num += 1
            batch += 1
        time.sleep(0.1)

if __name__ == "__main__":
    main()
