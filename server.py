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
    print("\t -mhost : Master Host address")
    print("\t -q     : Master Host port")
    print("\t -qport : Master Host port")

if __name__ == "__main__":
    from getopt import getopt, GetoptError
    from sys import argv,exit

    # Parse command line arguments, fail if option does not match or does not have value if required
    try:
        opts,args = getopt(argv[1:], 
                        shortopts='hs:p:tul:q:',
                        longopts=["help", "host=", "port=", "tcp", "udp", "log=", "mhost="])
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
        elif opt in ['-l', '--log']:
            log = logger(arg)
        elif opt in ['-m', '--mhost']:
            mhost = arg
        elif opt in ['-q', '--qport']:
            qport = int(arg)

    if not log:
        log = logger("")
    from lib.handler import update_log
    # Create and set global logger for client handlers
    update_log(log)

    from lib.tpc import init_response_thread, dest_response_thread
    # Check if master address sepcified, send a request for master to register peer
    if mhost:
        from lib.tcp_client import tcp_client
        from lib.operations import put

        tcp_client(log, mhost, qport, log, 3, "peer", "%s-%s" % (host,port))
        put("master", "%s-%d" % (mhost,qport))
        init_response_thread(log)

    # Initiate bind/listen seq for TCP/UDP as per selections
    connection_class(log, host, port)
    dest_response_thread()
