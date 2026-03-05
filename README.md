# Zero-to-Prod: Uptime & Observability Stack

## Architecture
- **Host A (Edge):** Nginx reverse proxy and TLS (16.176.172.158)
- **Host B (App):** Flask app and PostgreSQL primary((3.107.70.181)
- **Host C (Replica):** PostgreSQL DB replica (13.211.37.217)

## Task 1:  Infrastructure Setup
- Set up 3 EC2 Instances(Ubuntu 24.04, t3.micro) on AWS ap-southeast-02
- Hostnames configure to proper names on all hosts.
- All 3 instances can talk to each through the name resolution in /etc/hosts
- Network connections verified through using ping command to communicate within all the three hosts
- Security Groups configured : ports 22,80,443 open externally
  ICMP(for ping command) restricted to 172.31.0.0/16

## Task 2: Python application setup as ssystemd service
- Installed dependencies for python in Host B 
- Setup a python flask app that return json payload based on routes.(/opt/app) path in HOST B 
- Made flask application as a systemd service that runs without interruption.
- Enabled the ReStart on Failure so that it restarts after crashes or any issues.
- Enabled the flask service so that it runs always on startup and reboot.
- Proved restart-on-failure by killing the process with kill -9, 
  systemd automatically restarted with a new PID within 5 seconds


## Task 3: Installation of nginx as reverse proxy on Host A 
- Installed nginx on Host A
- Wrote nginx confoguration to forward request to the flask app running as service on HOST B 
- Generated TLS self signed certificate for HTTPS connection
- Added Inbound rule for Host B to open the port 5000
- Used duckdns to get a custom dns name for the site
- Verified TLS using openssl s_client - TLSv1.3 with AES-256-GCM cipher


## Task 4: Installing PostgreSQl and making it talk to Flask application.
- PostgreSQL installed on Host B
- Database and tables created for the PostgreSQL
- Flask application connected to PostgreSQL and updating the HEALTH_LOG table.


## Task 5: Install streaming replica on Host C
- PostgreSQL streaming replication configured
- Host C recieving real-time WAL stream data from Host B
- Data from database verified from both Host B and Host C
- checked pg_stat_replication and verifies active streaming connection.


## Task 6: Create a uptime monitoring script
- Create a shell script to check the health of the app.
- The healthcheck script hits the HTTP endpoint every minute
- Added it as a cronjob to make it run automatically
- Enabled script to capture reponsetime of the app in seconds
- verified the result by viewing it in real time using tail -f


## Task 7: Configure log rotation
- logrotate configured for healthcheck.sh script.
- Daily rotation with 7 days retention
- Compression working(healthcheck.log.gz)
- Forced log rotation verfied and working.
 

## Task 8:Alerting added to the healthcheck script.
- Created Alert log for seperation of failure logs from normal logs.
- Writing critical alerts to the systemd journal using logger in script.
- Simulated outage detected automatically in alert.log file as well as normal logs.
- Recovery also detected automatically in normal logs(healthcheck.log)


## Task 9: Added Status page that shows the real time logs
- created generate_status.sh script reads healthcheck.log and builds the HTML page
- Uptime is calculated automatically in percentage
- Served via nginx at https://suraj-devops.duckdns.org/status
- Runs automatically through cron job scheduled every minute
- Displays Last 10 healthchecks
