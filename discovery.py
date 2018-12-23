#
# Discovery service container
#
# Written by Glen Darling, December 2018.
# Copyright 2018, Glen Darling; all rights reserved.
#

from flask import Flask
import json
import socket
import sys
import threading
import time

# The data that will be published for this node goes here:
DATA_TO_PUBLISH = "Hello, World!"

# UDP server and cient
UDP_BIND_ADDRESS = '0.0.0.0'
UDP_PORT = 5959
UDP_BROADCAST = "255.255.255.255"
UDP_BUFFER_SIZE = 1024
discovered = []

# Configuration for the REST server
REST_API_BIND_ADDRESS = '0.0.0.0'
REST_API_PORT = 5960
REST_API_VERSION = "1.0"
webapp = Flask('discovery')

# UDP server to collect responses from other nodes running this software
class UdpListenThread(threading.Thread):
  def run(self):
    #print("\nLISTENER started!")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #print("Binding to address {}, port {}.".format(UDP_BIND_ADDRESS, UDP_PORT))
    sock.bind((UDP_BIND_ADDRESS, UDP_PORT))
    #print("Listening...")
    while True:
      data, address_and_port = sock.recvfrom(UDP_BUFFER_SIZE)
      address = address_and_port[0]
      js = { "address": str(address), "data": str(data) }
      # If it already exists in the array, remove the old entry
      for i in range(len(discovered)):
        if address == discovered[i]["address"]:
          del discovered[i]
      discovered.append(js)
      #print("\nDiscovered:\n{}".format(discovered))

# UDP client to publish our node data to other nodes running this software
class UdpPublishThread(threading.Thread):
  def run(self):
    #print("\nPUBLISHER started!  data: \"{}\"".format(self.getName()))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(5)
    data = self.getName()
    while True:
      #print("Sending to {}, port {}: \"{}\".".format(UDP_BROADCAST, UDP_PORT, self.getName()))
      sock.sendto(data.encode(), (UDP_BROADCAST, UDP_PORT))
      time.sleep(10)

# A web server to make the discovery data available locally
@webapp.route("/v1/discovered")
def get_discovered():
  out = { "version": REST_API_VERSION, "udp_port": UDP_PORT, "discovered": discovered }
  return json.dumps(out) + '\n'

# Main program (to instantiate and start the 3 threads)
if __name__ == '__main__':
  udp_listener = UdpListenThread()
  udp_publisher = UdpPublishThread(name = DATA_TO_PUBLISH)
  udp_listener.start()
  udp_publisher.start()
  webapp.run(host=REST_API_BIND_ADDRESS, port=REST_API_PORT)

