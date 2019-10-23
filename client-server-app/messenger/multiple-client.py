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
        cmd = ["python", "client.py"] + sys.argv[1:]
        process_list.append(Popen(" ".join(cmd), shell=True))
    return process_list


if __name__ == "__main__":
    process_list = []

    while True:
        action = input("(r)un new process / (c)lose all processes / (s)how clients / (q)uit\n")
        if action == "r":
            process_list.extend(_run_clients())
            continue

        if action == "c":
            _close_clients(process_list)
            process_list = []
            continue

        if action == "s":
            for proc in process_list:
                print(f"pid={proc.pid}, args='{proc.args}'")
            continue

        if action == "q":
            sys.exit()
