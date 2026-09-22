#!/usr/bin/env bash
# ==============================================================================
# 03_install_vpn.sh - Интерактивный установщик VPN решений
# ==============================================================================
set -euo pipefail

echo "========================================================="
echo "   Выберите протокол / решение для установки на VPS:"
echo "========================================================="
echo "1) 3X-UI Panel (Рекомендуется: VLESS-Reality, Trojan, Shadowsocks, веб-панель)"
echo "2) Marzban Node / Panel"
echo "3) AmneziaWG (Устойчивый к блокировкам WireGuard)"
echo "4) Sing-box (Standalone)"
echo "0) Выход"
echo "========================================================="
read -rp "Введите номер [1-4]: " choice

case "$choice" in
    1)
        echo "Установка 3X-UI..."
        bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
        ;;
    2)
        echo "Установка Marzban..."
        bash -c "$(curl -sL https://github.com/Gozargah/Marzban-scripts/raw/master/marzban.sh)" @ install
        ;;
    3)
        echo "AmneziaWG настраивается через клиент AmneziaVPN (https://amnezia.org) введя IP и root пароль."
        ;;
    4)
        echo "Установка официального Sing-box..."
        bash <(curl -fsSL https://sing-box.app/deb-install.sh)
        ;;
    *)
        echo "Отмена."
        ;;
esac
