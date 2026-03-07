# Troubleshooting Guide

## 1. Replica Connection Refused
**Symptom:** pg_stat_replication shows 0 rows
**Diagnose:**
1. Check replication status on primary:
   `sudo -u postgres psql -c "SELECT state, client_addr FROM pg_stat_replication;"`
2. Check replica logs:
   `sudo tail -20 /var/log/postgresql/postgresql-16-main.log`
3. Look for "Connection timed out" or "Connection refused" errors
4. Check firewall rules on replica:
   `sudo iptables -L INPUT`
   `sudo iptables -L OUTPUT`

**Fix:**
1. Remove blocking firewall rule:
   `sudo iptables -D OUTPUT 1`
2. Restart PostgreSQL on replica:
   `sudo systemctl restart postgresql`
3. Verify replication restored:
   `sudo -u postgres psql -c "SELECT state FROM pg_stat_replication;"`

## 2. TLS SNI Mismatch
**Symptom:** Browser shows "Your connection is not private". 
             Certificate CN doesn't match the domain.

**Diagnose:**
1. Check what certificate server is presenting:
   `curl -vk https://domain 2>&1 | grep subject`
2. If CN doesn't match domain → wrong certificate installed
3. Check Nginx config:
   `cat /etc/nginx/sites-available/suraj-devops`
4. Verify ssl_certificate path and server_name

**Fix:**
1. Update Nginx to correct certificate:
   `sudo nano /etc/nginx/sites-available/suraj-devops`
2. Ensure ssl_certificate points to correct .crt file
3. Ensure server_name matches certificate CN
4. Reload Nginx:
   `sudo nginx -t && sudo systemctl reload nginx`
5. Verify:
   `curl -vk https://domain 2>&1 | grep subject`


## 3. High Latency Alert Firing
**Symptom:** incidents.log shows P95 > 300ms

**Diagnose:**
1. Check incidents log:
   `cat /var/log/incidents.log`
2. Run alert manually to see current p95:
   `bash /opt/scripts/alert.sh`
3. Check if network delay is injected:
   `sudo tc qdisc show dev ens5`
4. Test latency directly:
   `curl -sk -w "%{time_total}" -o /dev/null https://suraj-devops.duckdns.org/app/health`
5. Check Flask app performance on Host B:
   `sudo systemctl status app`

**Fix:**
1. If tc netem delay injected — remove it:
   `sudo tc qdisc del dev ens5 root`
2. If Flask app slow — restart it:
   `sudo systemctl restart app`
3. Verify recovery:
   `bash /opt/scripts/alert.sh`
   Should show OK with p95 < 300ms
