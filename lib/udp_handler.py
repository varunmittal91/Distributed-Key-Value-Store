from .handler import handler
try:
    import socketserver
except ImportError:
    import SocketServer as socketserver

class udp_handler:
    def __init__(self, log, host, port):
        log.log(1, "Starting TCP server on Host: '%s' and Port: '%d'" % (host, port))
        socketserver.UDPServer.allow_reuse_address = True
        self.server = socketserver.UDPServer((host, port), handler)
        try:
            log.log(2, "Staring infinite loop")
            self.server.serve_forever()
        except:
            log.log(0, "Excetion, exiting loop")
            self.server.server_close()
