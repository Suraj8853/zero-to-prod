# Runbook — Zero-to-Prod Uptime & Observability Stack

## Architecture
- Host A (16.176.172.158) — Nginx reverse proxy, TLS, monitoring scripts
- Host B (3.107.70.181)   — Flask app, PostgreSQL primary
- Host C (13.211.37.217)  — PostgreSQL replica

## Key File Paths
- Flask app:        /opt/app/app.py
- Nginx config:     /etc/nginx/sites-available/suraj-devops
- Healthcheck:      /opt/scripts/healthcheck.sh, healthcheck.py
- Alert script:     /opt/scripts/alert.sh
- Backup script:    /opt/scripts/backup.sh
- Healthcheck log:  /opt/scripts/logs/healthcheck.log
- Incidents log:    /var/log/incidents.log
- DB backups:       /backup/YYYY/MM/DD/appdb.sql.gz

## Start/Stop Services
### Flask app (Host B)
- Start:   sudo systemctl start app
- Stop:    sudo systemctl stop app
- Status:  sudo systemctl status app
- Logs:    journalctl -u app -f

### Nginx (Host A)
- Start:   sudo systemctl start nginx
- Stop:    sudo systemctl stop nginx
- Reload:  sudo systemctl reload nginx
- Logs:    tail -f /var/log/nginx/access.log

### PostgreSQL (Host B and C)
- Start:   sudo systemctl start postgresql
- Stop:    sudo systemctl stop postgresql
- Status:  sudo systemctl status postgresql

## Health Checks
- Full stack:     curl -sk https://suraj-devops.duckdns.org/app/health
- Status page:    https://suraj-devops.duckdns.org/status
- DB metrics:     sudo -u postgres psql -d appdb -c "SELECT COUNT(*) FROM hc_metrics;"
- Replication:    sudo -u postgres psql -c "SELECT state, client_addr FROM pg_stat_replication;"

## Recovery Procedures

### Flask app down
1. ssh host-b
2. sudo systemctl status app
3. journalctl -u app --no-pager | tail -20
4. sudo systemctl restart app

### Replication broken
1. Check primary: sudo -u postgres psql -c "SELECT state FROM pg_stat_replication;"
2. Check replica logs: tail -20 /var/log/postgresql/postgresql-16-main.log
3. Check firewall: sudo iptables -L
4. Restart replica: sudo systemctl restart postgresql

### Restore database from backup
1. Find backup: ls /backup/YYYY/MM/DD/
2. Restore: gunzip -c /backup/YYYY/MM/DD/appdb.sql.gz | sudo -u postgres psql appdb 
