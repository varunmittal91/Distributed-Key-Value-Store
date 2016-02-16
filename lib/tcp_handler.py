import threading

from .handler import handler
try:
    import socketserver
except ImportError:
    import SocketServer as socketserver

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class tcp_handler:
    def __init__(self, log, host, port, mhost=None, qport=None):
        log.log(1, "Starting TCP server on Host: '%s' and Port: '%d'" % (host, port))
        socketserver.TCPServer.allow_reuse_address = True
        try:
            server  = ThreadedTCPServer((host, port), handler)
            host,port = server.server_address
            self.server = server
        except OSError:
            log.log(0, "Service already started on the given port")
            return
        # Check if master address sepcified, send a request for master to register peer
        if mhost:
            from .tcp_client import tcp_client
            from .operations import put
            from .tpc import init_response_thread, dest_response_thread

            tcp_client(log, mhost, qport, log, 3, "peer", "%s-%s" % (host,port))
            put("master", "%s-%d" % (mhost,qport))
            init_response_thread(log)
        try:
            log.log(2, "Staring infinite loop")
            self.server.serve_forever()
        except:
            # Capture event or cleanup seq like CTRL-C
            log.log(0, "Excetion, exiting loop")
            self.server.shutdown()
            self.server.server_close()
