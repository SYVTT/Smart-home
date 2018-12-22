#!/usr/bin/python3

import socket
import yaml

from wdsjn_function import parse_command

formal_language = yaml.load(open('V_4.yaml'))


def snd_cmd(data):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  s.sendto(data.encode('utf-8'), ('172.19.129.11', 1965))

  s.close()
# end def


def funkcja(tekst):
    result = parse_command(tekst, formal_language)
    return result
# end def


# Create socket and bind to address
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.bind(('',1964))

# Receive messages
while True:
  data,addr = UDPSock.recvfrom(1964)
  txt = data.decode('utf-8')
  print("<<",txt)
  cmd = funkcja(txt)
  print(">>",cmd)
  snd_cmd(cmd)
# end while

# Close socket
UDPSock.close()