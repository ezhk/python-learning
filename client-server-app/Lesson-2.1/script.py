#!/usr/bin/env python

from ipaddress import ip_network
from tabulate import tabulate
from socket import gethostbyname, gaierror
from subprocess import call, DEVNULL, TimeoutExpired


def host_port(hosts=[]):
    host_states = {}
    for host in hosts:
        try:
            destination_ip = gethostbyname(host)
        except gaierror as err:
            print(f"error resolve '{host}': {err}")
            host_states.update({host: "not resolved"})
            continue

        try:
            return_code = call(
                ("ping", "-q", "-c", "3", "-t", "3", host),
                timeout=5,
                stderr=DEVNULL,
                stdout=DEVNULL,
            )
        except TimeoutExpired as err:
            host_states.update({host: "check timeout"})
            continue

        status = "unavailable" if return_code else "alive"
        host_states.update({host: status})
    return host_states


def host_range_ping(net="127.0.0.0/31"):
    checking_hosts = ip_network(net).hosts()
    return host_port((ipaddr.compressed for ipaddr in checking_hosts))


if __name__ == "__main__":
    alive_hosts = host_range_ping("172.17.0.0/29")
    alive_hosts.update(host_port(["yandex.ru", "google.com"]))
    print(tabulate(alive_hosts.items(), headers=["Address", "Status"], tablefmt="fancy_grid"))

"""
╒════════════╤═════════════╕
│ Address    │ Status      │
╞════════════╪═════════════╡
│ 172.17.0.1 │ alive       │
├────────────┼─────────────┤
│ 172.17.0.2 │ unavailable │
├────────────┼─────────────┤
│ 172.17.0.3 │ alive       │
├────────────┼─────────────┤
│ 172.17.0.4 │ unavailable │
├────────────┼─────────────┤
│ 172.17.0.5 │ unavailable │
├────────────┼─────────────┤
│ 172.17.0.6 │ unavailable │
├────────────┼─────────────┤
│ yandex.ru  │ alive       │
├────────────┼─────────────┤
│ google.com │ alive       │
╘════════════╧═════════════╛
"""
