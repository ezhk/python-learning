#!/usr/bin/env python3

import sys
from subprocess import Popen


def _close_clients(processes):
    for proc in processes:
        proc.kill()
    return True


def _run_clients(count=1):
    process_list = []
    for _ in range(count):
        process_list.append(Popen("python client.py", shell=True))
    return process_list


if __name__ == "__main__":
    process_list = []

    while True:
        action = input("(r)un new processes / (c)lose all processes / (q)uit\n")
        if action == "q":
            sys.exit()

        if action == "c":
            _close_clients(process_list)
            process_list = []
            continue

        if action == "r":
            process_list.extend(_run_clients())
