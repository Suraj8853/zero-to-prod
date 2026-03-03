from flask import Flask,request,jsonify
import datetime
import socket

app = Flask(__name__)

@app.route('/health',methods=['GET'])
def health():
    return jsonify({
     "status": "ok",
      "ts": datetime.datetime.utcnow().isoformat(),
      "host":  socket.gethostname()

})

@app.route('/echo',methods=['POST'])
def echo():
     data = request.get_json(silent = True) or request.form.to_dict()
     return jsonify({"echo": data})


if __name__ ==  '__main__':
        app.run(host='0.0.0.0',port=5000)
