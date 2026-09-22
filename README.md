# 🚀 VPS VPN Setup & Management

Комплексный репозиторий для автоматической настройки, аудита и развертывания современных устойчивых протоколов VPN / Proxy (VLESS + Reality, Sing-box, Xray, WireGuard / Amnezia) на чистом VPS-сервере.

---

## 📊 Отчет о состоянии сервера (Audit Report)

- **IP-адрес**: `212.113.101.104`
- **Хостинг / Провайдер**: Aeza Network
- **ОС**: Debian GNU/Linux 13 (Trixie) x86_64
- **Ядро (Kernel)**: `6.12.85+deb13-amd64` (Актуальное современное ядро ветки 6.12)
- **CPU**: AMD Ryzen 9 5950X (1 vCPU)
- **RAM**: 3.8 GiB (доступно ~3.6 GiB, Swap отсутствует)
- **Диск**: 9.8 GB SSD (занято 905 MB / 10%, свободно 8.4 GB)
- **Сеть**: Поддерживает IPv4 и IPv6
- **TCP Congestion Control**: `cubic` (рекомендуется включить `BBR` для повышения скорости и снижения потерь пакетов)
- **Состояние ПО**: Требуется обновление 90 базовых пакетов (`apt update && apt upgrade -y`)

---

## 🛠 Быстрый старт: Подготовка сервера

### 1. Включение TCP BBR и оптимизация сети
```bash
# Включение алгоритма BBR для ускорения VPN-соединений
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p
```

### 2. Обновление системы и установка базовых утилит
```bash
apt update && apt upgrade -y
apt install -y curl wget git ufw htop jq tar socat fail2ban
```

---

## 🛡 Варианты развертывания VPN

### Вариант 1: 3X-UI (Xray Panel с веб-интерфейсом и VLESS Reality) — *Рекомендуемый*
3X-UI позволяет в удобном веб-интерфейсе создавать клиентов VLESS-Reality, Shadowsocks 2022, Trojan, WireGuard с QR-кодами и ссылками для v2rayN, Nekoray, Happ, Streisand, Hiddify.

Установка в одну команду:
```bash
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
```

### Вариант 2: Sing-box / Xray (Docker Compose)
В каталоге `docker/` представлены конфигурации для автономного запуска через Docker.

---

## 📂 Структура репозитория

```
vps_vpn/
├── README.md               # Документация и инструкции
├── scripts/
│   ├── 01_optimize_vps.sh  # Обновление пакетов, включение BBR, sysctl тюнинг
│   ├── 02_security.sh      # Настройка UFW, Fail2ban, SSH по ключам
│   └── 03_install_vpn.sh   # Меню установки VPN (3X-UI / Xray Reality / Amnezia)
├── docker/
│   ├── docker-compose.yml  # Развертывание сервисов в контейнерах
│   └── xray-reality/       # Конфигурация Xray Reality
└── .gitignore              # Исключение секретов и ключей
```

---

## 🔒 Безопасность

1. **SSH**: Рекомендуется отключить вход по паролю (`PasswordAuthentication no`) после добавления SSH-ключа в `~/.ssh/authorized_keys`.
2. **Фаервол (UFW)**: Открывайте только необходимые порты:
   ```bash
   ufw default deny incoming
   ufw default allow outgoing
   ufw allow 22/tcp
   ufw allow 443/tcp
   ufw allow 80/tcp
   ufw enable
   ```
3. **Секреты**: Никогда не коммитьте приватные ключи, токены или реальные пароли в публичный репозиторий.
