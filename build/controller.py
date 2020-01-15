#!/usr/bin/python3

import json
import sys
import socket
import signal
import time
from keywords import *
from parse_program import *

if len(sys.argv) < 3:
    print("usage: ./controller.py <port> <config>")
    exit(1)

testFile = sys.argv[2]
PORT = int(sys.argv[1])
if len(sys.argv)>=4:
    admin_password = sys.argv[3]
else:
    admin_password = b"admin"

if len(sys.argv) ==5:
    hub_password = sys.argv[4]
else:
    hub_password = b"hub_password"

def read_test(file=testFile):
    f = open(file, 'r')
    test = json.loads(f.read())
    f.close()
    return test


class controller():
    def __init__(self, input=1):
        self.text_input = input
        self.set_initial_states()
        self.principals = {}
        self.principals[b'admin'] = admin_password
        self.principals[b'hub'] = hub_password
        self.access = {}
    def get_input(self, _input):
        self.text_input = _input

    def parse_input(self):
        self.arguements = self.text_input[keys[0]]
        self.programs = self.text_input[keys[1]]
        # 

    def num_of_test_cases(self):
        return len(self.programs)

    def set_initial_states(self):
        self.configuration = read_test('config.json')
        self.sensors = {}
        self.devices = {}
        # print(self.configuration['sensors']['owner_location']\)
        for key in self.configuration['sensors'].keys():
            self.sensors[key] = int(self.configuration['sensors'][key])

        for key in self.configuration['output_devices'].keys():
            self.devices[key] = int(self.configuration['output_devices'][key])

    def generate_ouput(self, obj):
        status = parse_prog(self.text_input,obj )  # parse_program()
        print(status)
        return status

def sigterm_handler(signal, frame):
    # save the state here or do whatever you want
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

def main():
    host_ip = "localhost"
    wait = True
    obj = controller()
 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host_ip, PORT))
        s.listen()
        print('listening')
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                _input = conn.recv(4096)
                if _input:
                    obj.get_input(_input)
                    output = obj.generate_ouput(obj).encode()
                conn.sendall(output)

        print('connection terminated')
    print('end')


if __name__ == "__main__":
    main()
