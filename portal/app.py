#!/usr/bin/env python3
"""
VPS VPN Web Portal & Diagnostics API
"""

import os
import subprocess
from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    uptime = subprocess.getoutput("uptime -p")
    mem = subprocess.getoutput("free -h")
    bbr = subprocess.getoutput("sysctl -n net.ipv4.tcp_congestion_control")
    return jsonify({
        "server": "v3.idivles.ru",
        "ip": "212.113.101.104",
        "uptime": uptime,
        "memory": mem,
        "bbr": bbr,
        "status": "online"
    })

@app.route('/api/ping')
def api_ping():
    return jsonify({"status": "ok", "timestamp": os.times()[4]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
