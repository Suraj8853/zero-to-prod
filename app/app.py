from flask import Flask,request,jsonify
import datetime
import socket
import psycopg2 

app = Flask(__name__)
DB_URL = "dbname=appdb user=appuser password=apppass123 host=localhost"

def get_db():
    return psycopg2.connect(DB_URL)


@app.route('/health',methods=['GET'])
def health():
    try:
        conn = get_db()
        curr = conn.cursor()
        curr.execute("INSERT INTO health_log (status) VALUES (%s)",('ok',))
        conn.commit()
        curr.close()
        conn.close()
        db_status = "connected"
    except Exception as e:
          db_status = f"error: {str(e)}"
    return jsonify({
     "status": "ok",
      "ts": datetime.datetime.utcnow().isoformat(),
      "host":  socket.gethostname(),
       "db": db_status

})

@app.route('/echo',methods=['POST'])
def echo():
     data = request.get_json(silent = True) or request.form.to_dict()
     return jsonify({"echo": data})


if __name__ ==  '__main__':
        app.run(host='0.0.0.0',port=5000)
