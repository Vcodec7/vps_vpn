# 📱 Готовые конфигурации для подключения (Client Configs)

Домен сервера: **`v3.idivles.ru`** (IP: `212.113.101.104`)

---

## 1. ⚡ VLESS + XTLS-Reality (Основной / Рекомендуемый)

> **Преимущества**: Наивысшая скорость, нулевой оверхед, маскировка под настоящий трафик Google (`dl.google.com`), проходит любые DPI-фильтры.

```
vless://8cb32046-0d00-40c6-81c0-325bc1ac8fa4@v3.idivles.ru:443?type=tcp&security=reality&pbk=g6pfxKCDQFLpN1BKaSC-to-_orpUlP7WyiE9ATAfUxs&fp=chrome&sni=dl.google.com&sid=106ec6b5&flow=xtls-rprx-vision#VPS-VLESS-Reality
```

### Рекомендуемые приложения:
- **iOS**: [Happ](https://apps.apple.com/app/happ-proxy-utility/id6504287215), [Streisand](https://apps.apple.com/app/streisand/id6450534064), [FoXray](https://apps.apple.com/app/foxray/id6448898396)
- **Android**: [Happ](https://play.google.com/store/apps/details?id=com.happproxy), [v2rayNG](https://github.com/2dust/v2rayNG/releases), [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases)
- **Windows**: [v2rayN](https://github.com/2dust/v2rayN/releases), [Hiddify](https://github.com/hiddify/hiddify-next/releases), [Nekoray](https://github.com/MatsuriDayo/nekoray/releases)
- **macOS**: [FoXray](https://apps.apple.com/app/foxray/id6448898396), [Hiddify](https://github.com/hiddify/hiddify-next/releases), [V2Box](https://apps.apple.com/app/v2box-v2ray-client/id6446814043)

---

## 2. 🛡 WireGuard (Классический туннель)

Импортируйте в официальное приложение **WireGuard** или **AmneziaVPN**:

```ini
[Interface]
PrivateKey = SLcXGBmkqtmxAoTW6d0wd56XHAD29XWm/GNqaTmefm8=
Address = 10.8.0.2/24
DNS = 1.1.1.1, 8.8.8.8

[Peer]
PublicKey = ulrgbD+6G59BqcnRJDL357A1xMAQ8oBti/55BrjoNB4=
Endpoint = v3.idivles.ru:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

---

## 3. 🚀 Shadowsocks 2022

```
ss://YWVzLTEyOC1nY206enVwV0ZCZWhKaWROQTF5NUtic3ZiQUB2My5pZGl2bGVzLnJ1Ojg0NDM=#VPS-Shadowsocks
```

---

## 4. 🔒 Trojan TLS (с валидным Let's Encrypt SSL)

```
trojan://cd3a13d7-46fe-40d4-904b-e522fe459544@v3.idivles.ru:8444?security=tls&sni=v3.idivles.ru#VPS-Trojan-TLS
```

---

## 🌐 5. Веб-Панель 3X-UI

- **URL:** [https://v3.idivles.ru:2053/D11nS5my7qbNKjqt7L/](https://v3.idivles.ru:2053/D11nS5my7qbNKjqt7L/)
- **Логин:** `admin`
- **Пароль:** `AdminVpn2026!`
