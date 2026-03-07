# Demo Script — Zero-to-Prod Uptime & Observability Stack

## 1. Show the Architecture
Built a production-grade uptime and observability stack on AWS EC2 
from scratch. Three-host architecture with Nginx TLS reverse proxy 
on the edge, Flask application with PostgreSQL primary on the app 
server, and streaming replication to a replica for high availability. 
Includes automated health monitoring, SLO-based alerting, log parsing 
with p95 latency tracking, nightly backups, and a live status page.


┌─────────────────────────────────────────────────────────┐
│                        INTERNET                          │
└─────────────────────────┬───────────────────────────────┘
                          │ HTTPS (443)
                          ▼
┌─────────────────────────────────────────────────────────┐
│              HOST A - Edge (16.176.172.158)              │
│         Nginx Reverse Proxy + TLS + Monitoring           │
│                                                          │
│  healthcheck.sh  healthcheck.py  alert.sh  parse_logs.py│
└─────────────────────────┬───────────────────────────────┘
                          │ HTTP (5000) internal
                          ▼
┌─────────────────────────────────────────────────────────┐
│              HOST B - App (3.107.70.181)                 │
│           Flask App + PostgreSQL Primary                 │
│                                                          │
│         /opt/app/app.py    appdb (hc_metrics)           │
└─────────────────────────┬───────────────────────────────┘
                          │ Streaming Replication (5432)
                          ▼
┌─────────────────────────────────────────────────────────┐
│             HOST C - Replica (13.211.37.217)             │
│              PostgreSQL Streaming Replica                │
│                                                          │
│              pg_is_in_recovery() = true                 │
└─────────────────────────────────────────────────────────┘

## 2. Show HTTPS endpoint working (30 seconds)
curl -sk https://suraj-devops.duckdns.org/app/health

Expected output:
{"db":"connected","host":"host-b-app","status":"ok","ts":"..."}

## 3. Show TLS certificate (30 seconds)
openssl s_client -connect suraj-devops.duckdns.org:443 -servername suraj-devops.duckdns.org 2>&1 | grep -E "CN|TLS|Cipher"

Expected output:
TLSv1.3, Cipher TLS_AES_256_GCM_SHA384
CN=suraj-devops.duckdns.org

## 4. Show systemd service (30 seconds)
ssh host-b
sudo systemctl status app

## 5. Show database metrics (30 seconds)
sudo -u postgres psql -d appdb -c "SELECT COUNT(*), AVG(latency_ms) FROM hc_metrics;"

## 6. Show replication working (30 seconds)
sudo -u postgres psql -c "SELECT state, client_addr, replay_lag FROM pg_stat_replication;"

## 7. Show monitoring logs (30 seconds)
tail -10 /opt/scripts/logs/healthcheck.log

## 8. Show status page (30 seconds)
https://suraj-devops.duckdns.org/status

## 9. Simulate outage and recovery (60 seconds)
# Stop Flask
ssh host-b
sudo systemctl stop app

ssh host-a
bash /opt/scripts/alert.sh
cat /var/log/incidents.log

# Restart Flask
ssh host-b
sudo systemctl start app

# Verify recovery
curl -sk https://suraj-devops.duckdns.org/app/health
