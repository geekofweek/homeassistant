#!/bin/bash

CHECK=`grep -c "pubnub: take message interrupted" /home/_REDACTED_/.homeassistant/home-assistant.log`

if [ "$CHECK" == "0" ]
then
  echo "ok"
else
  echo "failed"
fi
