# 🛡 Руководство Администратора VPS VPN (`v3.idivles.ru`)

---

## 🔑 Учетные данные и доступ

| Сервис | Адрес / Ссылка | Логин / Идентификатор | Пароль / Токен |
| :--- | :--- | :--- | :--- |
| **Домен VPS** | `v3.idivles.ru` (`212.113.101.104`) | — | Let's Encrypt SSL Active |
| **SSH Доступ** | `v3.idivles.ru:22` | `root` | `dcc24e258f3a` |
| **3X-UI Веб-Панель** | `https://v3.idivles.ru:2053/D11nS5my7qbNKjqt7L/` | `admin` | `AdminVpn2026!` |
| **Telegram Бот** | Бот запущен на VPS | Admin ID: `8555955292` | `8626856754:AAGqy454SZaLuZ4ftY7yrRIf57nnv5eozbI` |
| **GitHub Репозиторий**| `https://github.com/Vcodec7/vps_vpn` | `Vcodec7` | `main branch` |

---

## ⚡ Развернутые протоколы и порты

| Протокол | Порт | Маскировка / Шифрование | Endpoint |
| :--- | :--- | :--- | :--- |
| **VLESS + Reality** | `443/tcp` | SNI: `dl.google.com`, Vision flow | `v3.idivles.ru:443` |
| **Shadowsocks 2022** | `8443/tcp,udp`| `aes-128-gcm` | `v3.idivles.ru:8443` |
| **Trojan TLS** | `8444/tcp` | Let's Encrypt SSL `v3.idivles.ru` | `v3.idivles.ru:8444` |
| **WireGuard** | `51820/udp` | ChaCha20-Poly1305 | `v3.idivles.ru:51820` |
| **3X-UI Web Panel** | `18550/tcp` | Защищенный путь `/D11nS5my7qbNKjqt7L/` | `v3.idivles.ru:18550` |

---

## 🤖 Управление через Telegram-Бота

Служба `vps-vpn-bot.service` на сервере автоматически выдает все ссылки и QR-коды уже с использованием домена **`v3.idivles.ru`**.
