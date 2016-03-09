#!/bin/env python

# Import local helper functions
from lib.tcp_client import tcp_client
from lib.udp_client import udp_client
from lib.logger import logger

def print_help(opt=None,arg=None):
    print("Usage:")
    print("\t --help : For help menu")
    print("\t -h     : For help menu")
    print("\t -s     : Host address")
    print("\t --host : Host address")
    print("\t -p     : Host port")
    print("\t --port : Host port")
    print("\t -t     : Connection mode: TCP")
    print("\t --tcp  : Connection mode: TCP")
    print("\t -u     : Connection mode: UDP")
    print("\t --udp  : Connection mode: UDP")
    print("\t -l     : Log level <info,debug>")
    print("\t -log   : Log level <info,debug>")
    print("\t -o     : Operation <0,1,2,3> 0:update, 1:GET, 2:DELETE, 3:PUT")
    print("\t --oprtn: Operation <0,1,2,3> 0:update, 1:GET, 2:DELETE, 3:PUT")
    print("\t -k     : Key")
    print("\t --key  : Key")
    print("\t -v     : Val")
    print("\t --val  : Val")

if __name__ == "__main__":
    from getopt import getopt, GetoptError
    from sys import argv,exit

    # Parse command line arguments, fail if option does not match or does not have value if required
    try:
        opts,args = getopt(argv[1:], shortopts='hs:p:tul:o:k:v:', 
                        longopts=["help", "host=", "port=", "tcp", "udp", "log=", "oprtn=", "val="])
    except GetoptError as e:
        print(e)
        print_help()
        exit(1)

    # Define defaults
    log   = logger("")
    oprtn = None
    key   = None
    val   = None

    host = "localhost"
    port = 9099
    connection_class = tcp_client
    for opt,arg in opts:
        if opt in ['-h', '--help']:
            print_help()
            exit(1)
        elif opt in ['-s', '--host']:
            host = arg
        elif opt in ['-p', '--port']:
            port = int(arg)
        elif opt in ['-u', '--udp']:
            connection_class = udp_client
        elif opt in ['-l', '--log']:
            log = logger(arg)
        elif opt in ['-o', '--oprtn']:
            try:
                oprtn = int(arg)
            except ValueError:
                log.log(0, "Operation should be an integer")
                print_help()
                exit(1)
        elif opt in ['-k', '--key']:
            key = arg
        elif opt in ['-v', '--val']:
            val = arg
                
    if oprtn == None:
        log.log(0, "No operation specified")
        print_help()
        exit(1)
    if not key:
        log.log(0, "No key specified")
        print_help()
        exit(1)
    elif oprtn not in [0,1,2,3]:
        log.log(0, "Operation out of range")
        print_help()
        exit(1)
    elif oprtn in [0,3] and not val:
        log.log(0, "Value required for this operation type")
        print_help()
        exit(1)

    # Initiate connect seq for TCP/UDP as per selections
    connection_class(log, host, port, log, oprtn, key, val, cclock=True)
