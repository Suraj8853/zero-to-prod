#!/usr/bin/env python3
import requests
import datetime
import time
import json
import os
import psycopg2
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
URL = "https://suraj-devops.duckdns.org/app/health"
DB_URL = "dbname=appdb user=appuser password=apppass123 host=host-b-app"
QUEUE_DIR = "/var/tmp/hc-queue"

os.makedirs(QUEUE_DIR,exist_ok=True)

def insert_metrics(ts,status,latency_ms):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO hc_metrics (ts,host,route,status,latency_ms) VALUES (%s, %s, %s, %s, %s)",(ts,"host-a-edge","/health",status,latency_ms))
    conn.commit();
    cur.close();
    conn.close();


def queue_metric(ts,status,latency_ms):
     filename = f"{QUEUE_DIR}/{ts.strftime('%Y%m%d%H%M%S')}.json"
     with open(filename,"w") as file:
              json.dump({
                   "ts": ts.isoformat(),
                    "status": status,
                    "latency_ms": latency_ms
                     },file)


def replay_queue():
    for filename in os.listdir(QUEUE_DIR):
        if not filename.endswith('.json'):
         continue
        filepath = os.path.join(QUEUE_DIR,filename)
        with open(filepath) as f:
          data = json.load(f)
          try:
               insert_metrics(datetime.datetime.fromisoformat(data['ts']),data['status'],data['latency_ms'])
               os.remove(filepath)
               print(f"Removed {filename}")

          except Exception as e:
                  print(F"Replay Failed: ",e)
                  break




def run():
    ts = datetime.datetime.utcnow()
    start = time.time()
    try:
        response = requests.get(URL,verify=False,timeout=10)
        status = response.status_code
    except Exception:
           status = 0
    latency_ms = round((time.time() - start)*1000,2)
    
    try:
        replay_queue()
        insert_metrics(ts,status,latency_ms)
        print(f"{ts} OK {status} - {latency_ms}ms")
        
    except Exception as e:
           print(f"{ts} DB down queueing: {e} ")
           queue_metric(ts,status,latency_ms)

if __name__ == '__main__':
    run()
