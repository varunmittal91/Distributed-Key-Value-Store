#!/bin/env bash

function test_key_val_store {
    mode=$1
    # Start server in tcp mode and send to background
    ./server.py $mode -l debug &
    # pid of the server, cleanup after test
    pid=$!

    # Sleeping for a second to make sure server init has completed
    sleep 1

    # Creating arbitary key pairs
    ./client.py $mode -l debug -o 3 -k "key1" -v "val1"
    ./client.py $mode -l debug -o 3 -k "key2" -v "val2"
    ./client.py $mode -l debug -o 3 -k "key3" -v "val3"
    ./client.py $mode -l debug -o 3 -k "key4" -v "val4"
    ./client.py $mode -l debug -o 3 -k "key5" -v "val5"

    # Verify data with def key-value pairs
    ./client.py $mode -l debug -o 1 -k "key1"
    ./client.py $mode -l debug -o 2 -k "key1"
    ./client.py $mode -l debug -o 1 -k "key1"

    # Generating random values for predefined keys
    ./client.py $mode -l debug -o 3 -k "new_key1" -v `openssl rand -base64 32`
    ./client.py $mode -l debug -o 3 -k "new_key2" -v `openssl rand -base64 32`
    ./client.py $mode -l debug -o 3 -k "new_key3" -v `openssl rand -base64 32`
    ./client.py $mode -l debug -o 3 -k "new_key4" -v `openssl rand -base64 32`
    ./client.py $mode -l debug -o 3 -k "new_key5" -v `openssl rand -base64 32`

    # Retrieving random values for predefined keys
    ./client.py $mode -l debug -o 1 -k "new_key1"
    ./client.py $mode -l debug -o 1 -k "new_key2"
    ./client.py $mode -l debug -o 1 -k "new_key3"
    ./client.py $mode -l debug -o 1 -k "new_key4"
    ./client.py $mode -l debug -o 1 -k "new_key5"

    # Cleaning up random values
    ./client.py $mode -l debug -o 2 -k "new_key1"
    ./client.py $mode -l debug -o 2 -k "new_key2"
    ./client.py $mode -l debug -o 2 -k "new_key3"
    ./client.py $mode -l debug -o 2 -k "new_key4"
    ./client.py $mode -l debug -o 2 -k "new_key5"

    kill -9 $pid
}

# Run test case in UDP mode
test_key_val_store "-u"
# Run test case in TCP mode
test_key_val_store "-t"
