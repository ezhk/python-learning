#!/usr/bin/env python

import mongoengine
import matplotlib.pyplot as plt
import numpy

from server.jim.config import STORAGE
from server.jim.models import Users, Messages


def f_cos(x):
    return x * 2 - numpy.cos(x)


def f_sqrt(x):
    return x ** 3 - numpy.sqrt(x)


if __name__ == "__main__":
    conn = mongoengine.connect(host=STORAGE)

    users, messages_count = [], []
    for value in (
        {
            "username": Users.objects(id=x["_id"]).first().username,
            "count": x["count"],
        }
        for x in Messages.objects().aggregate(
            {"$group": {"_id": "$author", "count": {"$sum": 1}}}
        )
    ):
        users.append(value["username"])
        messages_count.append(value["count"])
        print(f"User {value['username']} has sent {value['count']} message(s)")

    conn.close()

    max_value = max(messages_count)
    max_index = messages_count.index(max_value)

    explode = [0] * len(users)
    explode[max_index] = 0.05

    # DB pie graph
    _, ax1 = plt.subplots()
    ax1.pie(
        messages_count,
        explode=explode,
        labels=users,
        autopct="%1.2f%%",
        shadow=False,
        startangle=0,
    )
    ax1.axis("equal")
    ax1.set_title("Messages per user")

    # Functions graphs
    values = numpy.arange(-30, 30, 0.2)
    plt.figure()
    ax2 = plt.subplot(211)
    ax2.set_title("y = x*2 - cos(x)")
    ax2.plot(values, f_cos(values), "k")
    ax2.grid(True)

    values = numpy.arange(0, 10, 0.2)
    ax3 = plt.subplot(212)
    ax3.set_title("y = x^3 - sqrt(x)")
    ax3.plot(values, f_sqrt(values), "r--")
    ax3.grid(True)

    plt.subplots_adjust(hspace=0.5)
    plt.show()
