#!/usr/bin/python3

import json
import sys
import socket
from keywords import *
from parse_program import *
if len(sys.argv) != 3:
    print("usage: ./controller.py <test> <port>")
    exit(1)

testFile = sys.argv[1]
PORT = int(sys.argv[2])


def read_test():
    f = open(testFile, 'r')
    test = json.loads(f.read())
    f.close()
    return test


class controller():
    def __init__(self, input=1):
        self.text_input = input
        # self.parse_input()
        # self.set_initial_states()

    def get_input(self, _input):
        self.text_input = _input

    def parse_input(self):
        self.arguements = self.text_input[keys[0]]
        self.programs = self.text_input[keys[1]]
        self.configuration = self.text_input[keys[2]]

    def num_of_test_cases(self):
        return len(self.programs)

    def set_initial_states(self):
        self.sensors = {}
        self.devices = {}
        # print(self.configuration['sensors']['owner_location']\)
        for key in self.configuration['sensors'].keys():
            print('key:', key)
            self.sensors[key] = int(self.configuration['sensors'][key])

        for key in self.configuration['output_devices'].keys():
            self.devices[key] = int(self.configuration['output_devices'][key])

    def generate_ouput(self):
        status = parse_prog(self.text_input)  # parse_program()
        print(status)
        return status


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
                    print(_input)
                    print('received')
                    output = obj.generate_ouput().encode()
                conn.sendall(output)

        print('connection terminated')
    print('end')


if __name__ == "__main__":
    main()
