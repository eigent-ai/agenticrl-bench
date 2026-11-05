#!/usr/bin/env python3
import os
import time


def main():
    metrics_file = "/opt/monitor/data/metrics.log"
    relay_file = "/opt/monitor/data/relay.log"

    while not os.path.exists(metrics_file):
        time.sleep(1)

    with open(metrics_file, 'r') as infile:
        while True:
            line = infile.readline()
            if line:
                relayed = "[relayed] {}\n".format(line.strip())
                with open(relay_file, 'a') as outfile:
                    outfile.write(relayed)
            else:
                time.sleep(1)


if __name__ == "__main__":
    main()
