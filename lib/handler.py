try:
    import socketserver
except ImportError:
    import SocketServer as socketserver

# Parse string and extract oprtn,key,val pair
from .operations import decode_HEADER
log = None

# Set global loger
def update_log(in_log):
    global log
    log = in_log

class handler(socketserver.BaseRequestHandler):
    def handle(self):
        import threading
        cur_thread = threading.current_thread()
        caddr,cport = self.client_address
        global log
        log.log(1, "Recieved request from Host: '%s', Port: '%d'" % (caddr, cport))
        try:
            data = self.request.recv(1024)
            response = decode_HEADER(log, data)
            request = self.request
            request.send(response)
        except AttributeError:
            data,request = self.request
            response = decode_HEADER(log, data)
            request.sendto(response, (caddr,cport))
