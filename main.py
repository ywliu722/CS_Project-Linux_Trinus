#!/bin/python3

import logging
from time import sleep

#from callback.open_vr import OpenVR
from callback.mouse import Mouse
from discover import discover
from frame_generator import FrameGenerator
from sender import Sender
from sensor_client import SensorClient

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    server_ip = discover()
    server_port = 6666
    client_port = 7777

    sender = Sender(server_ip, server_port=server_port, client_port=client_port)

    # Run frame generator for sender
    framegen = FrameGenerator(sender.settings, sender.framebuf)
    framegen.start()

    # Start sending frames to client
    sender.start()

    # Wait for sensor server init
    sleep(1)

    client = SensorClient(
        #server_ip, server_port=server_port, callback_objects=[OpenVR()]
	    server_ip, server_port=server_port, callback_objects=[Mouse()]
    )
    client.start()

    client.join()
    sender.join()
    framegen.join()


if __name__ == "__main__":
    main()
