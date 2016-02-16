# Client helper to convert oprtn,key,val in a string and send to server and recieve response
def exchange_mssg(s, log, oprtn, key, val, values=None):
    mssg = "%d:%s:%s" % (oprtn, key, val)
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
        status,message = data.split(b':')
    except ValueError:
        log.log(0, "Server Error, recieved an empty response")
        return
    # If status not 0, operation failed
    if status != b"0":
        log.log(0, message)
    else:
        log.log(1, message)
        if oprtn == 1:
            print("Value: %s" % message)
            if values != None:
                values.append((key,message))
    s.close()
    return data
