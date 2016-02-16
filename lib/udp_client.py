import socket
from .client import exchange_mssg

class udp_client:
    def __init__(self, log, host, port, *args, **kwargs):
        log.log(1, "Connecting to UDP Server on Host: '%s', Port: '%d'" % (host, port))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((host, port))
        exchange_mssg(s, *args, **kwargs)
