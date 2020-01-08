#! /usr/bin/env python3

"""
This server program stores the information from the different water stations.
It creates database DATABASE, asks from the water stations for information by
sending the KEEPALIVE_MSG massage, and saves the information to DATABASE.
"""

from socket import *
from copy import copy
import time
import sqlite3

KEEPALIVE_MSG = "keep alive"
DATABASE = "data.db"
setdefaulttimeout(0)

# connect to the database
with sqlite3.connect(DATABASE) as db:
    cursor = db.cursor()

    # create table if not exists
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS station_status ("
            "station_id INT UNIQUE,"
            "last_date TEXT,"
            "alarm1 INT,"
            "alarm2 INT,"
             "PRIMARY KEY(station_id));")

    # create socket connection
    with socket() as s:

        s.bind(('', 65432))
        s.listen(16)

        # list of the connected clients
        client_list = []
        print("waiting on {}:{}".format(*s.getsockname()))

        while True:

            try:
                # wait for connections
                c, addr = s.accept()

            except OSError:
                pass

            else:
                # add water station to the list
                print("{}:{} connected".format(*addr))
                client_list.append((c,addr))

            # for each station that connected: get data from the station, update the
            # stations database and send keep a live massage
            for client in copy(client_list):

                try:
                    # get data from water station
                    msg = client[0].recv(1024).decode()

                except OSError:
                    pass

                else:

                    if len(msg) == 0:

                        # if the station disconnected, remove it from the list
                        print('{}:{} has disconnected'.format(*client[1]))
                        client_list.remove(client)

                    else:

                        # update stations data base
                        # print('{}:{} --> "{}"'.format(*client[1], msg))
                        msg = msg.split()
                        id = int(msg[0])
                        last_date = msg[1] + " " + msg[2]
                        alarm1 = int(msg[3])
                        alarm2 = int(msg[4])
                        cursor.execute("INSERT OR REPLACE INTO station_status VALUES(?,?,?,?)",(id,last_date,alarm1,alarm2))

                        # send keep alive massage to the station
                        client[0].send(KEEPALIVE_MSG.encode())

            # commit changes to the database
            db.commit()

            # wait 60 seconds before next update
            time.sleep(10)

