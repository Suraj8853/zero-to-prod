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
