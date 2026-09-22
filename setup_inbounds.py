import sqlite3
import json
import time

conn = sqlite3.connect('/etc/x-ui/x-ui.db')
c = conn.cursor()

# 1. Update general settings
c.execute("UPDATE settings SET value='2053' WHERE key='webPort'")
c.execute("UPDATE settings SET value='/D11nS5my7qbNKjqt7L/' WHERE key='webBasePath'")
c.execute("UPDATE settings SET value='/9k7xuvoxldiq5zsh/' WHERE key='subPath'")
c.execute("UPDATE settings SET value='2096' WHERE key='subPort'")
c.execute("UPDATE settings SET value='http://[2a0b:4140:e510::2]:2096/9k7xuvoxldiq5zsh/' WHERE key='subURI'")

# Update credentials
c.execute("UPDATE users SET username='admin', password='AdminVpn2026!' WHERE id=1")

# Clear old inbounds and clients
c.execute("DELETE FROM inbounds")
c.execute("DELETE FROM client_traffics")
try:
    c.execute("DELETE FROM clients")
except:
    pass

# Reality Settings with valid X25519 keypair
reality_stream_settings = {
    "network": "tcp",
    "security": "reality",
    "realitySettings": {
        "show": False,
        "xver": 0,
        "dest": "gateway.icloud.com:443",
        "serverNames": [
            "gateway.icloud.com",
            "www.apple.com",
            "www.microsoft.com"
        ],
        "privateKey": "mGHq2yBNW25gLT1TO4UgrjOEcGdxAbq9wzzrXsBOZVc",
        "minClientVer": "",
        "maxClientVer": "",
        "maxTimediff": 0,
        "shortIds": [
            "106ec6b5",
            "",
            "a1b2c3d4"
        ],
        "settings": {
            "publicKey": "7UErqWH58efvIsbqzUTTMhekB1Va_xhdD3wn8BRZ6HU",
            "fingerprint": "chrome",
            "serverName": "",
            "spiderX": "/"
        }
    },
    "tcpSettings": {
        "acceptProxyProtocol": False,
        "header": {
            "type": "none"
        }
    }
}

client_obj = {
    "id": "8cb32046-0d00-40c6-81c0-325bc1ac8fa4",
    "flow": "xtls-rprx-vision",
    "email": "default_user",
    "limitIp": 0,
    "totalGB": 0,
    "expiryTime": 0,
    "enable": True,
    "tgId": "",
    "subId": "0861ace1ba5cd059",
    "reset": 0
}

inbound_settings = {
    "clients": [client_obj],
    "decryption": "none",
    "fallbacks": []
}

sniffing_settings = {
    "enabled": True,
    "destOverride": ["http", "tls", "quic", "fakedns"]
}

c.execute("""
INSERT INTO inbounds (
    id, user_id, up, down, total, remark, enable, expiry_time,
    listen, port, protocol, settings, stream_settings, tag, sniffing
) VALUES (
    1, 1, 0, 0, 0, '⚡ VLESS Reality (443)', 1, 0,
    '', 443, 'vless', ?, ?, 'inbound-443', ?
)
""", (json.dumps(inbound_settings), json.dumps(reality_stream_settings), json.dumps(sniffing_settings)))

# Insert client_traffics
c.execute("""
INSERT INTO client_traffics (
    inbound_id, enable, email, up, down, expiry_time, total, reset
) VALUES (
    1, 1, 'default_user', 0, 0, 0, 0, 0
)
""")

# Shadowsocks Inbound (Port 8443)
ss_settings = {
    "method": "2022-blake3-aes-128-gcm",
    "password": "zV9Q6m9yV3u5g7y9j2K4m6P8r1T3w5y7",
    "network": "tcp,udp"
}
ss_stream = {"network": "tcp"}
c.execute("""
INSERT INTO inbounds (
    id, user_id, up, down, total, remark, enable, expiry_time,
    listen, port, protocol, settings, stream_settings, tag, sniffing
) VALUES (
    2, 1, 0, 0, 0, '🛡️ Shadowsocks 2022 (8443)', 1, 0,
    '', 8443, 'shadowsocks', ?, ?, 'inbound-8443', ?
)
""", (json.dumps(ss_settings), json.dumps(ss_stream), json.dumps(sniffing_settings)))

conn.commit()
conn.close()
print("3X-UI inbounds configured successfully!")
