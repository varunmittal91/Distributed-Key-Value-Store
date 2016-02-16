import socket
from .client import exchange_mssg

class tcp_client:
    def __init__(self, log, host, port, *args, **kwargs):
        log.log(1, "Connecting to TCP Server on Host: '%s', Port: '%d'" % (host, port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, port))
            exchange_mssg(s, *args, **kwargs)
        except socket.error:
            log.log(0, "Connection failed")
            return
        log.log(1, "Operation completed")
