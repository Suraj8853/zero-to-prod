#!/usr/bin/env python3
import re
import gzip
import os
import csv
import datetime
from collections import defaultdict

LOG_DIR = "/var/log/nginx"
REPORT_DIR = "/opt/scripts/report"

LOG_PATTERN = re.compile(
    r'(\d+\.\d+\.\d+\.\d+).*\[(.+?)\].*"(\w+) (\S+) HTTP.*?" (\d+) \d+ ".*?" ".*?" rt=(\d+\.\d+)'
)

def read_log_file(filepath):
    if filepath.endswith('.gz'):
        with gzip.open(filepath, 'rt') as f:
            return f.readlines()
    else:
        with open(filepath, 'r') as f:
            return f.readlines()

def parse_logs():
    records = []
    ip_counts = defaultdict(int)
    for filename in sorted(os.listdir(LOG_DIR)):
        if 'access' not in filename:
            continue
        filepath = os.path.join(LOG_DIR, filename)
        lines = read_log_file(filepath)
        for line in lines:
            match = LOG_PATTERN.search(line)
            if not match:
                continue
            ip, ts, method, route, status, rt = match.groups()
            records.append({
                'ip': ip,
                'ts': ts,
                'method': method,
                'route': route,
                'status': int(status),
                'rt': float(rt)
            })
            ip_counts[ip] += 1
    return records, ip_counts

def generate_report(records, ip_counts):
    if not records:
        print("No records found")
        return
    total = len(records)
    ok = sum(1 for r in records if r['status'] < 400)
    errors_4xx = sum(1 for r in records if 400 <= r['status'] < 500)
    errors_5xx = sum(1 for r in records if r['status'] >= 500)
    availability = round((ok / total) * 100, 2)
    latencies = sorted(r['rt'] for r in records)
    p95_index = int(len(latencies) * 0.95)
    p95 = round(latencies[p95_index] * 1000, 2)
    top_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"Total requests:  {total}")
    print(f"Availability:    {availability}%")
    print(f"p95 latency:     {p95}ms")
    print(f"4xx errors:      {errors_4xx}")
    print(f"5xx errors:      {errors_5xx}")
    print(f"Top IPs:         {top_ips}")

def write_csv(records):
    if not records:
        return
    today = datetime.date.today().strftime('%Y-%m-%d')
    filepath = f"{REPORT_DIR}/{today}.csv"
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['ip','ts','method','route','status','rt'])
        writer.writeheader()
        writer.writerows(records)
    print(f"CSV written to {filepath}")

if __name__ == '__main__':
    records, ip_counts = parse_logs()
    generate_report(records, ip_counts)
    write_csv(records)
