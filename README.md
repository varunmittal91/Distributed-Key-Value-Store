# Distributed-Key-Value-Store

## Communication Atomicity
Atomicity is maintained by using Two-phase-commit

## Code Organization
The key value store has been implemented in Python. The code is compatible with both python2
and python3. Though python3 is recommended due to better unicode support and handling. 
 
The code is organized as following 
.
├── client.py                 \\ main wrapper function for client
├── lib
│   ├── client.py             \\ exchange operation details and data for both tcp/udp
│   ├── handler.py            \\ server program handling request
│   ├── __init__.py           \\ dummy file, to mark library in python
│   ├── logger.py             \\ universal logger, accepts 0­error, 1­info, 2­debug
│   ├── operations.py         \\ lambda functions for operations
│   ├── tcp_client.py         \\ Initiate tcp connection
│   ├── tcp_handler.py        \\ Server library to create and listen in TCP mode
│   ├── tpc.py                \\ Two Phase Commit negotiator
│   ├── udp_client.py         \\ Initiate udp connection
│   ├── udp_handler.py        \\ Server library to create and listen in UDP mode
├── server.py
└── test.sh

 
## Running
To   test   the   project,   ./test.sh   can   be   used.   It   has   a   function   that   initiates   server   first   in   
UDP   mode  
and   tests   with   instances   of   clients   and   then   in   TCP   mode.   At   the   end   of   the   test   it   sends   
kill  
signal to server instances that were started in background.  
The   bash   script   is   written   in   a   way   that   starts   both   server   and   client   in   debug   mode   by   
default.  
One   portion   of   test   has   been   written   to   generate   random   values   using   openssl,   which   should   be  
present in majority of UNIX like operating systems and Windows if it were any more considerate. 
 
“Running test”  
$ ./test.sh 
 
### Help
Server   and   client   can   be   started   independently   and   have   been   incorporated   with   detailed   help  
option. 
./serve --help
./clie --help
 
Common attributes: 
 ­s/­­host: host address/IP 
 ­p/­­port: host port 
 ­t/­­tcp  : tcp mode 
 ­u/­­udp: udp mode 
 ­l/­­log  : log level, info/debug 
Client attributes: 
  ­o/­­oprtn: 0:update, 1:get, 2:delete, 3:put 
  ­k/­­key    : key   ­v/­­val    : value 

