## Distributed-Key-Value-Store
The key value store has been implemented in Python. The code is compatible with both python2
and python3. Though python3 is recommended due to better unicode support and handling. 
 
### Communication Atomicity
Atomicity is maintained by using Two-phase-commit

### Master/Slave configuration
By Default the server is designed to run as master.<br>
However, if server is started with "-m" or "--mhost", then it automatically becomes a slave and sends a registration request to 
the master.<br>
After the registration is successful, master will send requests to the new peer and wait for ack for vote/commit operation in 
case of any write/update to the server.<br>

### Code Organization
The code is organized as following 

| File | Function |
|------|----------|
|client.py         |main wrapper function for client|
|lib/client.py     |exchange operation details and data for both tcp/udp|
|lib/handler.py    |server program handling request|
|lib/\__init\__.py |dummy file, to mark library in python
|lib/logger.py     |universal logger, accepts 0­error, 1­info, 2­debug
|lib/operations.py |lambda functions for operations
|lib/tcp_client.py |Initiate tcp connection
|lib/tcp_handler.py|Server library to create and listen in TCP mode
|lib/tpc.py        |Two Phase Commit negotiator
|lib/udp_client.py |Initiate udp connection
|lib/udp_handler.py|Server library to create and listen in UDP mode
|server.py         |main wrapper function for server|
|test.sh           |test script for UNIX environment to start server and then run random put/delete and finally close server|

 
## Starting server and running tests
To test the project, ./test.sh can be used. It has a function that initiates server first in UDP mode and tests with instances   
of clients and then in TCP mode. At the end of the test it sends kill signal to server instances that were started in 
background.<br>
The bash script is written in a way that starts both server and client in debug mode by default. <br>
A prt of test has been written to generate random values using openssl, which should be present in majority of UNIX like 
operating systems and Windows if it were any more considerate. <br>
 
"Executing test”  
$ ./test.sh 
 
### Help
Server and client can be started independently and have been incorporated with detailed help option. <br>
./server --help<br>
./client --help<br>

