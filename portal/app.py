#!/usr/bin/env python3
"""
VPS VPN Web Portal & Diagnostics API
"""

import os
import base64
import subprocess
from flask import Flask, render_template, jsonify, request, Response

app = Flask(__name__, template_folder='templates')

# Pre-defined robust configs
VLESS_REALITY_IPV6 = "vless://8cb32046-0d00-40c6-81c0-325bc1ac8fa4@[2a0b:4140:e510::2]:443?type=tcp&security=reality&pbk=7UErqWH58efvIsbqzUTTMhekB1Va_xhdD3wn8BRZ6HU&fp=chrome&sni=gateway.icloud.com&sid=106ec6b5&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20VPS%20%E2%9A%A1%20IPv6%20Reality%20(iCloud)"
VLESS_REALITY_IPV4 = "vless://8cb32046-0d00-40c6-81c0-325bc1ac8fa4@212.113.101.104:443?type=tcp&security=reality&pbk=7UErqWH58efvIsbqzUTTMhekB1Va_xhdD3wn8BRZ6HU&fp=chrome&sni=gateway.icloud.com&sid=106ec6b5&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20VPS%20%E2%9A%A1%20IPv4%20Reality%20(iCloud)"
VLESS_REALITY_MS_IPV6 = "vless://8cb32046-0d00-40c6-81c0-325bc1ac8fa4@[2a0b:4140:e510::2]:443?type=tcp&security=reality&pbk=7UErqWH58efvIsbqzUTTMhekB1Va_xhdD3wn8BRZ6HU&fp=chrome&sni=www.microsoft.com&sid=106ec6b5&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20VPS%20%E2%9A%A1%20IPv6%20Reality%20(Microsoft)"
SHADOWSOCKS_IPV6 = "ss://MjAyMi1ibGFrZTMtYWVzLTEyOC1nY206elY5UTZtOXlWM3U1Zzd5OWoySzRtNlA4cjFUM3c1eTc=@%5B2a0b:4140:e510::2%5D:8443#%F0%9F%9B%A1%EF%B8%8F%20VPS%20%F0%9F%94%92%20Shadowsocks-2022%20IPv6"
SHADOWSOCKS_IPV4 = "ss://MjAyMi1ibGFrZTMtYWVzLTEyOC1nY206elY5UTZtOXlWM3U1Zzd5OWoySzRtNlA4cjFUM3c1eTc=@212.113.101.104:8443#%F0%9F%9B%A1%EF%B8%8F%20VPS%20%F0%9F%94%92%20Shadowsocks-2022%20IPv4"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sub')
@app.route('/sub/<path:sub_id>')
def subscription(sub_id="default"):
    # Return Base64 encoded configs for Happ, Streisand, v2rayNG, sing-box
    configs = f"{VLESS_REALITY_IPV6}\n{VLESS_REALITY_IPV4}\n{VLESS_REALITY_MS_IPV6}\n{SHADOWSOCKS_IPV6}\n{SHADOWSOCKS_IPV4}\n"
    b64_data = base64.b64encode(configs.encode('utf-8')).decode('utf-8')
    return Response(b64_data, mimetype='text/plain', headers={
        'Subscription-Userinfo': 'upload=0; download=0; total=1073741824000; expire=0',
        'Profile-Update-Interval': '24'
    })

@app.route('/api/status')
def api_status():
    uptime = subprocess.getoutput("uptime -p")
    mem = subprocess.getoutput("free -h")
    bbr = subprocess.getoutput("sysctl -n net.ipv4.tcp_congestion_control")
    return jsonify({
        "server": "v3.idivles.ru",
        "ipv4": "212.113.101.104",
        "ipv6": "2a0b:4140:e510::2",
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
