#!/bin/bash
URL="https://suraj-devops.duckdns.org/"
LOGFILE="/var/log/healthcheck.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

RESPONSE=$(curl -sk -o /dev/null -w "%{http_code} %{time_total}" $URL)

if [[ "$RESPONSE" = "200" ]]; then
echo "$TIMESTAMP OK HTTP $RESPONSE" >> $LOGFILE
else
echo "$TIMESTAMP OK HTTP $RESPONSE" >> $LOGFILE
fi

