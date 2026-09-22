#!/usr/bin/env bash
# ==============================================================================
# 02_security.sh - Базовая настройка безопасности (UFW + Fail2ban)
# ==============================================================================
set -euo pipefail

echo "===> [1/2] Настройка UFW (Uncomplicated Firewall)..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing

# Разрешаем SSH
ufw allow 22/tcp comment 'SSH'

# Разрешаем стандартные порты веб/VPN
ufw allow 80/tcp comment 'HTTP / ACME'
ufw allow 443/tcp comment 'HTTPS / VLESS Reality'
ufw allow 443/udp comment 'QUIC / Hysteria2'
ufw allow 2053/tcp comment '3X-UI Web Panel Default'

# Включаем UFW
echo "y" | ufw enable
ufw status verbose

echo "===> [2/2] Настройка Fail2ban..."
systemctl enable --now fail2ban
systemctl restart fail2ban

echo "===> Настройка безопасности завершена!"
