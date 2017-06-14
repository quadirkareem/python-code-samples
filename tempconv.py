#!/usr/bin/env python

import argparse

def print_usage()
    print("usage: %s -fob <job_name> -b|--branch <branch_name> [-")

def to_celsius(fahrenheit)
    return (fahrenheit - 32) * (5/9)
    
def to_fahrenheit(celsius)
    return (celsius + 32) * (9/5)
    
def get_cmd_line_args()
    if len(sys.argv) == 0
        print_usage()
        exit 1
    
def main()
    get_cmd_line_args()
    
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()