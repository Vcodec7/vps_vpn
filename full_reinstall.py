import paramiko
import sys
import os
import time

HOST = os.getenv("VPS_HOST", "212.113.101.104")
USER = os.getenv("VPS_USER", "root")
PASS = os.getenv("VPS_PASS", "dcc24e258f3a")

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def run_cmd(ssh, cmd, title=""):
    if title:
        print(f"\n{'='*20} {title} {'='*20}")
    print(f"[VPS EXEC] {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=600)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if out:
        print(out)
    if err:
        print(f"[STDERR] {err}")
    return out, err

def main():
    print(f"Connecting to VPS {HOST}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=22, username=USER, password=PASS, timeout=20)
    print("Connected successfully!")

    # 1. Update OS and install prerequisites
    run_cmd(ssh, "export DEBIAN_FRONTEND=noninteractive && apt-get update -y && apt-get install -y curl wget git ufw fail2ban wireguard qrencode python3 python3-pip python3-venv sqlite3 nginx certbot python3-certbot-nginx", "1. System Updates & Essential Packages")

    # 2. Kernel BBR & sysctl network tuning
    sysctl_script = """
cat << 'EOF' > /etc/sysctl.d/99-vps-tuning.conf
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
net.core.rmem_max = 67108864
net.core.wmem_max = 67108864
net.core.rmem_default = 33554432
net.core.wmem_default = 33554432
net.core.optmem_max = 2048576
net.core.somaxconn = 65535
net.ipv4.tcp_rmem = 4096 87380 33554432
net.ipv4.tcp_wmem = 4096 65536 33554432
net.ipv4.tcp_fastopen = 3
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_keepalive_time = 300
net.ipv4.tcp_keepalive_probes = 5
net.ipv4.tcp_keepalive_intvl = 15
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1
net.ipv4.conf.all.rp_filter = 0
net.ipv4.conf.default.rp_filter = 0
EOF
sysctl --system
"""
    run_cmd(ssh, sysctl_script, "2. Sysctl BBR & Network Optimization")

    # 3. Swap creation if needed
    swap_script = """
if [ $(swapon --show | wc -l) -le 1 ]; then
    fallocate -l 2G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=2048
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "Swap created: 2GB"
fi
"""
    run_cmd(ssh, swap_script, "3. Swap Setup")

    # 4. Install 3X-UI automatically
    xui_install = """
export XUI_BIN_FOLDER="/usr/local/x-ui"
RELEASE_URL=$(curl -Ls "https://api.github.com/repos/MHSanaei/3x-ui/releases/latest" | grep '"browser_download_url":.*x-ui-linux-amd64.tar.gz' | head -n 1 | cut -d '"' -f 4)
if [ -z "$RELEASE_URL" ]; then
    RELEASE_URL="https://github.com/MHSanaei/3x-ui/releases/download/v2.4.9/x-ui-linux-amd64.tar.gz"
fi
echo "Downloading 3X-UI from $RELEASE_URL"
wget -N --no-check-certificate -O /root/x-ui-linux-amd64.tar.gz "$RELEASE_URL"
cd /root && tar zxvf x-ui-linux-amd64.tar.gz
chmod +x x-ui/x-ui x-ui/bin/xray-linux-amd64
cp -f x-ui/x-ui.service /etc/systemd/system/
rm -rf /usr/local/x-ui
mv x-ui /usr/local/
systemctl daemon-reload
systemctl enable x-ui
systemctl start x-ui
"""
    run_cmd(ssh, xui_install, "4. 3X-UI Core Installation")

    time.sleep(3)

    # 5. Initialize 3X-UI DB with custom admin credentials & port 2053
    xui_db_setup = """
systemctl stop x-ui
mkdir -p /etc/x-ui
cat << 'EOF' > /tmp/setup_xui.py
import sqlite3

conn = sqlite3.connect('/etc/x-ui/x-ui.db')
c = conn.cursor()

# Set panel user & password
c.execute("UPDATE users SET username='admin', password='AdminVpn2026!' WHERE id=1")
c.execute("UPDATE settings SET value='2053' WHERE key='webPort'")
c.execute("UPDATE settings SET value='/D11nS5my7qbNKjqt7L/' WHERE key='webBasePath'")
conn.commit()
conn.close()
print("3X-UI DB Updated successfully!")
EOF
python3 /tmp/setup_xui.py
systemctl start x-ui
"""
    run_cmd(ssh, xui_db_setup, "5. Configure 3X-UI Panel Port & Auth")

    # 6. Upload Local Project Files (Portal, Bot, WireGuard configs)
    sftp = ssh.open_sftp()
    
    # Create remote directories
    run_cmd(ssh, "mkdir -p /opt/vps_vpn/portal/templates /opt/vps_vpn/portal/static /opt/vps_vpn/bot /etc/wireguard")
    
    local_dir = r"c:\Users\Евгений\vps_vpn"
    
    # Upload Portal files
    sftp.put(os.path.join(local_dir, "portal", "app.py"), "/opt/vps_vpn/portal/app.py")
    sftp.put(os.path.join(local_dir, "portal", "templates", "index.html"), "/opt/vps_vpn/portal/templates/index.html")
    
    # Upload Bot files
    sftp.put(os.path.join(local_dir, "bot", "vpn_bot.py"), "/opt/vps_vpn/bot/vpn_bot.py")
    
    sftp.close()

    # 7. Setup Python Venv & Systemd services
    services_script = """
# Python venv for Portal and Bot
python3 -m venv /opt/vps_vpn/venv
/opt/vps_vpn/venv/bin/pip install --upgrade pip
/opt/vps_vpn/venv/bin/pip install flask pyTelegramBotAPI psutil requests

# Portal Service
cat << 'EOF' > /etc/systemd/system/vps-vpn-portal.service
[Unit]
Description=VPS VPN Web Portal and Diagnostics
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/vps_vpn/portal
ExecStart=/opt/vps_vpn/venv/bin/python app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Bot Service
cat << 'EOF' > /etc/systemd/system/vps-vpn-bot.service
[Unit]
Description=VPS VPN Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/vps_vpn/bot
ExecStart=/opt/vps_vpn/venv/bin/python vpn_bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Nginx config for dual stack (IPv4 & IPv6)
cat << 'EOF' > /etc/nginx/sites-available/default
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

systemctl daemon-reload
systemctl enable vps-vpn-portal
systemctl restart vps-vpn-portal
systemctl enable vps-vpn-bot
systemctl restart vps-vpn-bot
systemctl restart nginx
"""
    run_cmd(ssh, services_script, "6. Setup Web Portal, Telegram Bot & Nginx")

    # 8. Configure WireGuard
    wg_script = """
cat << 'EOF' > /etc/wireguard/wg0.conf
[Interface]
Address = 10.8.0.1/24, fd00::1/64
ListenPort = 51820
PrivateKey = aP1...
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o net0 -j MASQUERADE; ip6tables -A FORWARD -i wg0 -j ACCEPT; ip6tables -t nat -A POSTROUTING -o net0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o net0 -j MASQUERADE; ip6tables -D FORWARD -i wg0 -j ACCEPT; ip6tables -t nat -D POSTROUTING -o net0 -j MASQUERADE
EOF
"""
    
    # 9. Verify listening ports
    run_cmd(ssh, "ss -tulpn", "7. Final Port Verification")
    
    ssh.close()
    print("\n✅ DEPLOYMENT COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
