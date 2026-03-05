#!/bin/bash

URL="https://suraj-devops.duckdns.org/app/health"
LOGFILE="/opt/scripts/logs/healthcheck.log"
ALERTLOG="/opt/scripts/logs/alerts.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

RESPONSE=$(curl -sk -o /dev/null -w "%{http_code} %{time_total}" "$URL")
HTTP_CODE=$(echo $RESPONSE | cut -d' ' -f1)
TIME=$(echo $RESPONSE | cut -d' ' -f2)

if [ "$HTTP_CODE" = "200" ]; then
    echo "$TIMESTAMP OK - HTTP $HTTP_CODE - ${TIME}s" >> "$LOGFILE"
else
    echo "$TIMESTAMP FAIL - HTTP $HTTP_CODE - ${TIME}s" >> "$LOGFILE"
    echo "$TIMESTAMP CRITICAL - Service down! HTTP $HTTP_CODE" >> "$ALERTLOG"
    logger -t healthcheck "CRITICAL: $URL returned HTTP $HTTP_CODE"
fi

