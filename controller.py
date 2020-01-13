#!/usr/bin/python

import json
import sys
from keywords import *

testFile = sys.argv[1]


def read_test():
    f = open( testFile, 'r')
    test = json.loads( f.read())
    f.close()
    return test



 
class controller():
    def __init__(self):
        self.text_input = read_test()
        self.parse_input()
    
    def parse_input(self):
        self.arguements = self.text_input[keys[0]]
        self.programs = self.text_input[keys[1]]
        self.configuration = self.text_input[keys[2]]

	def set_initial_config(self):
		print('initial config')

    # def generate_ouput(self):

    #   for prog in progs:
       
    #       results = "["
    #       oneline=False
    #       for line in readlines(s):
    #           print(line)
    #           if (oneline):
    #               results += ", "
    #           results += line
    #           oneline = True
    #       results += "]"


def main():
	obj = controller()


if __name__ == "__main__":
	main()