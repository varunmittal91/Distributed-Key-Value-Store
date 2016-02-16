#!/bin/bash

echo "deploying on local machine"
pkill -9 python
rm -rf code && rm -rf log && mkdir -p ~/{code,log} && cp code.zip code && cd code && unzip code.zip && rm code.zip
cd

echo "deploying on n03"
scp code.zip n03:~
ssh n03 "rm -rf ~/code/ && mkdir -p ~/{code,log} && cp code.zip code && cd code && unzip code.zip && rm code.zip && pkill -9 
python"

echo "deploying on n04"
scp code.zip n04:~
ssh n04 "rm -rf ~/code/ && mkdir -p ~/{code,log} && cp code.zip code && cd code && unzip code.zip && rm code.zip && pkill -9 
python"

echo "deploying on n05"
scp code.zip n05:~
ssh n05 "rm -rf ~/code/ && mkdir -p ~/{code,log} && cp code.zip code && cd code && unzip code.zip && rm code.zip && pkill -9 
python"

echo "deploying on n06"
scp code.zip n06:~
ssh n06 "rm -rf ~/code/ && mkdir -p ~/{code,log} && cp code.zip code && cd code && unzip code.zip && rm code.zip && pkill -9 
python"

echo "deploying on n07"
scp code.zip n07:~
ssh n07 "rm -rf ~/code/ && mkdir -p ~/{code,log} && cp code.zip code && cd code && unzip code.zip && rm code.zip && pkill -9 
python"

echo "deploying on n08"
scp code.zip n08:~
ssh n08 "rm -rf ~/code/ && mkdir -p ~/{code,log} && cp code.zip code && cd code && unzip code.zip && rm code.zip && pkill -9 
python"

echo "deploying on n09"
scp code.zip n09:~
ssh n09 "rm -rf ~/code/ && mkdir -p ~/{code,log} && cp code.zip code && cd code && unzip code.zip && rm code.zip && pkill -9 
python"

./code/exec.py --dir ~/code/ --host_list ~/hostlist --start --logfile ~/log/server.log --host n01

