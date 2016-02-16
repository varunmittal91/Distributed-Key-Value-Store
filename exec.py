#!/bin/env python2

def help():
    from sys import exit
    print "Help"
    print "\t-h         : This Message"
    print "\t--host     : host address for coordinator"
    print "\t--port     : port number  for coordinator"
    print "\t--host_list: list of hosts"
    print "\t--start    : start cluster"
    print "\t--stop     : stop  cluster"
    print "\t--logfile  : logfile path for all servers"
    exit(1)

def read_opts():
    from sys import argv
    from getopt import getopt, GetoptError

    try:
        opts,args = getopt(argv[1:], "h", ["host=", "port=", "dir=", "host_list=", "logfile=", "start", "stop"])
    except GetoptError as e:
        print e
        help()
    return opts

def start():
    pass

if __name__=="__main__":
    opts = read_opts()

    host_list_file = None
    host = "localhost"
    port = "9099"
    dir  = None
    mode = None
    logfile = None
    for opt,arg in opts:
        if opt == '-h':
            help()
        elif opt == "--host_list":
            host_list_file = arg
        elif opt == "--host":
            host = arg
        elif opt == "--port":
            port = arg
        elif opt == "--dir":
            dir = arg
        elif opt == "--logfile":
            logfile = arg
        elif opt == "--start":
            mode = "start"
        elif opt == "--stop":
            mode = "stop"
    if not mode:
        print "Mode required, --start --stop"
        help()
    if not dir:
        print "Base directory required"
        help()
    if not host_list_file:
        print "Host file list needed"
        help()
    try:
        file  = open(host_list_file)
        hosts = [peer_host[:-1] for peer_host in file.readlines()]
    except IOError:
        print "Unable to open host_list_file"

    import subprocess
    cmd = ["%s/server.py" % dir, "--host", "0.0.0.0", "--port", port, "-l", "debug"]
    if logfile:
        cmd.extend(["--logfile", logfile])
    subprocess.Popen(cmd)
    for peer_host in hosts:
        cmd = ["ssh", "-C", peer_host, "%s/server.py" % dir, "--host", "0.0.0.0", "--port", "0", "-l", "debug",
                   "--mhost", host, "--qport", port]
        if logfile:
            cmd.extend(["--logfile", logfile])
        subprocess.Popen(cmd)
