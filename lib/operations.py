key_val_store = {}

def put(key, data, client_addr=None):
    if key == "__all__":
        import json
        return 0, json.dumps(key_val_store)
    elif key == "peer":
        try:
            host,port = data.split('-')
            # Extract host from client_addr, as visible to coordinator
            host = client_addr['host']
            id = "%s-%s" % (host,port)
            try:
                if id not in key_val_store["peer"]:
                    key_val_store["peer"].append(id)
            except KeyError:
                key_val_store["peer"] = [id]
        except ValueError:
            return 1, "Peer registration failed invalid with invalid data:%s" % data
        return 0, "Peer registered"
    elif key == "vote":
        from .tpc import queue_response

        uuid = data
        # Get master host,port for sending ack and send ack
        mhost,qport = key_val_store.get('master').split('-')
        # Queue response ack with uuid
        queue_response(3, "ack", uuid, mhost, qport)

        return 0, "Recieved vote sending ack"
    elif key == "ack":
        uuid = data
        try:
            key_val_store["ack:%s" % uuid].append("")
        except KeyError:
            key_val_store["ack:%s" % uuid] = [""]
        return 0, "Acknoledged %s" % uuid
    elif key.startswith("req_ack"):
        from .tpc import queue_response
        try:
            uuid,key = key.split('=')[1:]
            # Get master host,port for sending ack and send ack
            mhost,qport = key_val_store.get('master').split('-')
            # Queue response ack with uuid
            queue_response(3, "ack", uuid, mhost, qport)
        except ValueError:
            return 0, "Malformed request for ack_req type operation"
    key_val_store[key] = data
    return "0", "Added"

def get(key, data, client_addr=None):
    if key == b"peer":
        import json
        return "0", json.dumps([id for id in key_val_store.get("peer", [])])
    try:
        return "0", key_val_store[key]
    except KeyError:
        return "1", "key does not exist"

def update(key, data, client_addr=None):
    try:
        key_val_store[key]
        key_val_store[key] = data
        return "0", "updated"
    except KeyError:
        return "1", "key does not exist"

def delete(key, data, client_addr=None):
    try:
        key_val_store.pop(key)
        return "0", "deleted"
    except KeyError:
        return "1", "key does not exist"

# Lambda function dictionary
oprtns = {
    0: [update, True],
    1: [get   , False],
    2: [delete, True],
    3: [put   , True],
}

def prepare_response(status, reason, current_clock):
    return ("%d:%s:%d" % (status, reason, current_clock)).encode()

# Helper function to read oprtn and call appropriate lambda function
def decode_HEADER(log, client_addr, header):
    from .clock import get_clock,update_clock 
    # Get current clock
    current_clock = get_clock()
    # Try extracting values or fail with error message
    try:
        # Get client clock
        header,cclock = header.split(b'==')
        # If it is a client and not slave responding do not check clock 
        if int(cclock) != -1:
            if current_clock > int(cclock):
                return prepare_response(1, "Clock out of sync", current_clock)
            update_clock(int(cclock)+1)
    except:
        log.log(0, "client did not send the clock")
        return prepare_response(1, "No clock recieved", current_clock)
        return b"1:No clock recieved:%d" % current_clock

    try:
        oprtn,key,val = header.split(b':')
        key = key.decode()
        val = val.decode()
    except:
        log.log(0, "Invalid operation or malformed request")
        return current_clock(1, "Invalid input", current_clock)
        return b"1:Invalid input"
    log.log(2, "Receieved request, OPRTN:%s, key:%s, val:%s, client_clock:%s, current_clock:%d" % 
            (oprtn, key, val, cclock, current_clock))
    oprtn = int(oprtn)
    fnc,tpc = oprtns[oprtn]

    peers = key_val_store.get("peer", [])
    if tpc and peers and key not in ['ack', 'peer']:
        from .tpc import get_uuid,vote,commit,check_ack

        # Generate unique identifier for tracking vote and acks
        uuid = get_uuid()
        
        # Conduct vote and add to queue
        vote(log, uuid, peers)
        if check_ack(log, uuid, len(peers), key_val_store.get, delete):
           # Commit, generating new uuid
           uuid = get_uuid()
           commit(log, uuid, peers, oprtn, key, val)
           status,message = 0,"Commit completed"
           if not check_ack(log, uuid, len(peers), key_val_store.get, delete):
               status,message = 1,"All acks not received"
        else:
           status,message = 1,"All acks not received"
    elif oprtn == 1 and peers:
        from lib.tcp_client import tcp_client

        log.log(2, "Requesting key: '%s' from peers" % key)
        values = []
        for peer in peers:
            host,port = peer.split('-')
            tcp_client(log, host, int(port), log, oprtn, key, None, values=values)
        values = [val for key,val in values if val]
        try:
            status,message = 0, values[0]
        except IndexError:
            status,message = 1, "Key not found or data corrupted"
    elif oprtn == 1 and key == "__all__":
        import json
        return prepare_response(0, json.dumps(key_val_store), current_clock)
    else:
        status,message = fnc(key,val,client_addr)
        
    log.log(2, b"Completed request")
    return prepare_response(int(status), message, current_clock)
    return ("%s:%s" % (int(status),message)).encode()
