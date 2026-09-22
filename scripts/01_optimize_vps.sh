#!/usr/bin/env bash
# ==============================================================================
# 01_optimize_vps.sh - Системная оптимизация Debian/Ubuntu VPS
# ==============================================================================
set -euo pipefail

echo "===> [1/4] Обновление репозиториев и системы..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get upgrade -y
apt-get autoremove -y

echo "===> [2/4] Установка базовых утилит..."
apt-get install -y --no-install-recommends \
    curl wget git ufw htop jq tar socat ca-certificates \
    gnupg lsb-release net-tools fail2ban

echo "===> [3/4] Включение алгоритма TCP BBR..."
if ! grep -q "net.core.default_qdisc=fq" /etc/sysctl.conf; then
    echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
fi
if ! grep -q "net.ipv4.tcp_congestion_control=bbr" /etc/sysctl.conf; then
    echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
fi

# Оптимизация сетевого стека для VPN
cat << 'EOF' > /etc/sysctl.d/99-vpn-optimization.conf
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1
net.core.rmem_max = 67108864
net.core.wmem_max = 67108864
net.core.rmem_default = 65536
net.core.wmem_default = 65536
net.core.netdev_max_backlog = 10000
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864
net.ipv4.tcp_mtu_probing = 1
EOF

sysctl --system

echo "===> [4/4] Создание Swap-файла (1GB) для стабильности при пиках памяти..."
if [ ! -f /swapfile ]; then
    fallocate -l 1G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=1024
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "vm.swappiness=10" >> /etc/sysctl.d/99-vpn-optimization.conf
    sysctl vm.swappiness=10
fi

echo "===> Оптимизация успешно завершена!"
