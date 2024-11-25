#!/bin/bash

source hisse/bin/activate
python3 notifyTelegram.py &>/dev/null &

process_id=`/bin/ps -fu $USER| grep "notifyTelegram.py" | grep -v "grep" | awk '{print $2}'`

echo $process_id > pid
