#!/usr/bin/python

# ***************************************************************
# Copyright (C) 2016 CipherCloud, Inc. All Rights Reserved.
# This software is the confidential and proprietary information
# of CipherCloud, Inc. ("Confidential Information").
# For more information, visit http://www.ciphercloud.com
# ***************************************************************

# ==============================================================
# This script is used to build docker image
#
# author: Quadir Sha Kareemullah
# ==============================================================

import sys
import argparse
import subprocess

DEFAULT_TAG_NAME = 'latest'
REGISTRIES={ 'idc': 'idc-registry.ciphercloud.local:5000',
             'eqnx': 'registry.ciphercloud.local:5000',
             'qa-hub': 'hub.qa.ciphercloud.net:5000',
             'hub': 'hub.ciphercloud.net:5000'
            }
DOCKER_BUILD_CMD = [ "docker", "build", "-t", "cc-jre8", "." ]

# ---------------------------------------------------------------
# this function executes commands
# ---------------------------------------------------------------
def exec_cmd(cmd_arr): 
   subprocess.check_call(cmd_arr)

# ---------------------------------------------------------------
# this function parses and returns command line arguments
# ---------------------------------------------------------------
def get_cmd_args(): 
   parser = argparse.ArgumentParser(description='Build Docker image')
   parser.add_argument('-t', '--tag', default=DEFAULT_TAG_NAME, help='Docker image tag name')
   parser.add_argument('-r', '--registry', help='Docker Registry Server', 
                        choices=REGISTRIES.keys())

   return parser.parse_args()

# ---------------------------------------------------------------
# MAIN function
# ---------------------------------------------------------------
def main():
   #args = get_cmd_args()

   #exec_cmd(DOCKER_BUILD_CMD)
   tag = ''.join(args.tag.split()).lower()
   
   if [ tag
   
   sys.exit(0)

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# EXECUTE - script execution starts here
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
if __name__ == "__main__":
   main()

