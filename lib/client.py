from .clock import get_clock,update_clock

# Client helper to convert oprtn,key,val in a string and send to server and recieve response
def exchange_mssg(s, log, oprtn, key, val, values=None, cclock=False):
    cclock = get_clock() if cclock == False else cclock
    mssg = "%d:%s:%s==%d" % (oprtn, key, val, cclock)
    # Send string
    s.send(mssg.encode())
    try:
        # Wait for response
        data = s.recv(1024)
    except ConnectionRefusedError:
        log.log(0, "Cannot recieve data, connection lost")
        return
    # server replies with status and message
    try:
        status,message,sclock = data.split(b':')
        sclock = int(sclock)
    except ValueError:
        log.log(0, "Server Error, recieved an empty response")
        return
    # If status not 0, operation failed
    if status != b"0":
        from .tcp_client import tcp_client
        if message == b'Clock out of sync':
            from .operations import key_val_store
            mhost,qport = key_val_store['master'].split('-')
            qport = int(qport)
            update_clock(sclock+1)
            tcp_client(log, mhost, qport, log, 1, "__all__", val)
        log.log(0, message)
    else:
        log.log(1, message)
        if oprtn == 1:
            if values != None:
                values.append((key,message))
    s.close()
    return data
