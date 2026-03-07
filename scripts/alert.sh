#!/bin/bash

DB_HOST="host-b-app"
DB_NAME="appdb"
DB_USER="appuser"
DB_PASS="apppass123"
INCIDENTS_LOG="/var/log/incident.log"
TIMESTAMP=$(date +'%Y-%m-%d %H:%M:%S')
ALERT=0
ALERT_MSG=""

RESULT=$(PGPASSWORD=$DB_PASS psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "
SELECT
    COUNT(*) as total,
    SUM(CASE WHEN status = 200 THEN 1 ELSE 0 END) as ok,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms) as p95
FROM hc_metrics
WHERE ts > NOW() - INTERVAL '15 minutes';
")

TOTAL=$(echo $RESULT | awk '{print $1}')
OK=$(echo $RESULT | awk '{print $3}')
P95=$(echo $RESULT | awk '{print $5}')

if [ -z "$TOTAL" ] || [ "$TOTAL" -eq 0 ]; then
echo "$TIMESTAMP No Data in last 15 mins" >> $INCIDENTS_LOG
exit 0
fi

AVAILABILITY=$(awk "BEGIN {printf \"%.2f\",($OK/$TOTAL)*100}")
if (( $(echo "$AVAILABILITY < 99.5 "| bc -l) )); then
 ALERT=1
 ALERT_MSG="$ALERT_MSG AVAILABILITY=${AVAILABILITY}% (threshold 99.5%)"
fi

if (( $(echo "$P95 > 300"  | bc -l) )); then
ALERT=1
ALERT_MSG="$ALERT_MSG P95=${P95}ms (threshold 300ms)"
fi

if [ "$ALERT" -eq 1 ]; then
echo "$TIMESTAMP critical -$ALERT_MSG" >> $INCIDENTS_LOG
logger -t alert "CRITICAL:$ALERT_MSG"
echo "TIMESTAMP CRITICAL: $ALERT_MSG"
else
echo "TIMESTAMP OK- availablity=${AVAILABILITY}% p95=${P95}ms"
fi

