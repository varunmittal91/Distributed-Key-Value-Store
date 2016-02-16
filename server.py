#!/bin/env python

# Import local helper functions
from lib.udp_handler import udp_handler
from lib.tcp_handler import tcp_handler
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
    print("\t -m     : Master Host address")
    print("\t --mhost: Master Host address")
    print("\t -q     : Master Host port")
    print("\t --qport: Master Host port")
    print("\t --logfile: Logfile path")

if __name__ == "__main__":
    from getopt import getopt, GetoptError
    from sys import argv,exit

    # Parse command line arguments, fail if option does not match or does not have value if required
    try:
        opts,args = getopt(argv[1:], 
                        shortopts='hs:p:tul:q:',
                        longopts=["help", "host=", "port=", "tcp", "udp", "log=", "mhost=", "qport=", "logfile="])
    except GetoptError as e:
        print(e)
        print_help()
        exit(1)

    log = None

    host = "localhost"
    port = 9099

    # Coordinator/Master host address
    mhost = None
    # Coordinator/Master host port, default set to 9099
    qport = 9099

    # log level
    loglevel = None
    # log file
    logfile = None    

    connection_class = tcp_handler
    for opt,arg in opts:
        if opt in ['-h', '--help']:
            print_help()
            exit(1)
        elif opt in ['-s', '--host']:
            host = arg
        elif opt in ['-p', '--port']:
            port = int(arg)
        elif opt in ['-u', '--udp']:
            connection_class = udp_handler
        elif opt in ['-m', '--mhost']:
            mhost = arg
        elif opt in ['-q', '--qport']:
            qport = int(arg)
        elif opt in ['-l', '--log']:
            loglevel = arg
        elif opt == "--logfile":
            logfile = arg

    if not loglevel:
        log = logger("")
    else:
        log = logger(loglevel, logfile)
    from lib.handler import update_log
    # Create and set global logger for client handlers
    update_log(log)

    from lib.tpc import dest_response_thread

    # Initiate bind/listen seq for TCP/UDP as per selections
    connection_class(log, host, port, mhost, qport)
    dest_response_thread()
