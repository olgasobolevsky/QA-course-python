#! /usr/bin/env python3

"""
This client program is a water station representation. It waits for the request from the server
(keep a live massage) ,reads data from file FILENAME and sends it to the server SERVER_ADDRESS.
The data is: station identifier, current date, status of first alarm
and status of second alarm
"""
from socket import *
from datetime import datetime

SERVER_ADDRESS = ('127.0.0.1',65432)
FILENAME = "status.txt"
KEEPALIVE_MSG = "keep alive"

with socket() as s:
    # connect to the server
    s.connect(SERVER_ADDRESS)

    server_msg = KEEPALIVE_MSG

    while True:

        # open file FILENAME and read station id, alarm1 status and alarm2 status
        if server_msg == KEEPALIVE_MSG:
            with open(FILENAME) as file:
                try:
                    station_id, alarm1, alarm2 = file.readlines()
                except ValueError:
                    # if the file FILENAME has less than 3 lines, exit the program
                    print("Error: Wrong format of the {} file".format(FILENAME))
                    break
            station_id = station_id.replace("\n", "")
            alarm1 = alarm1.replace("\n", "")
            alarm2 = alarm2.replace("\n", "")

            # Create universal format for current date and time
            date = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M')

            # Prepare massage to send to the server
            msg = station_id+" "+date+" "+alarm1+" "+alarm2

            # Send the massage to the server
            # print("sending :{}".format(msg))
            s.send(msg.encode())

        # wait for keep alive massage from server
        try:
            server_msg = s.recv(1024).decode()

        # if the connection to the server is lost, exit the program
        except ConnectionResetError:
            print("Error: Can't connect to the server")
            break




