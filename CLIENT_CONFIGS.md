# 📱 Готовые конфигурации для подключения (Client Configs)

Все протоколы уже настроены на сервере `212.113.101.104`. Вы можете импортировать ссылки ниже в любое поддерживаемое приложение.

---

## 1. ⚡ VLESS + XTLS-Reality (Основной / Рекомендуемый)

> **Преимущества**: Наивысшая скорость, нулевой оверхед, маскировка под настоящий трафик Google (`dl.google.com`), проходит любые DPI-фильтры.

```
vless://f3923284-03eb-4920-839a-9195af363bca@212.113.101.104:443?type=tcp&security=reality&pbk=8umwn2l_7CTOfHkc9eIzLW-alojT5Nlrpi0Aa_ssmGY&fp=chrome&sni=dl.google.com&sid=2a7136af&flow=xtls-rprx-vision#VPS-VLESS-Reality
```

### Рекомендуемые приложения:
- **iOS**: [Happ](https://apps.apple.com/app/happ-proxy-utility/id6504287215), [Streisand](https://apps.apple.com/app/streisand/id6450534064), [FoXray](https://apps.apple.com/app/foxray/id6448898396)
- **Android**: [Happ](https://play.google.com/store/apps/details?id=com.happproxy), [v2rayNG](https://github.com/2dust/v2rayNG/releases), [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases)
- **Windows**: [v2rayN](https://github.com/2dust/v2rayN/releases), [Hiddify](https://github.com/hiddify/hiddify-next/releases), [Nekoray](https://github.com/MatsuriDayo/nekoray/releases)
- **macOS**: [FoXray](https://apps.apple.com/app/foxray/id6448898396), [Hiddify](https://github.com/hiddify/hiddify-next/releases), [V2Box](https://apps.apple.com/app/v2box-v2ray-client/id6446814043)

---

## 2. 🛡 WireGuard (Классический туннель)

Сохраните следующий текст в файл `vps_vpn.conf` и импортируйте в официальное приложение **WireGuard** или **AmneziaVPN**:

```ini
[Interface]
PrivateKey = cP9PCbdWcKGi0wg8Zq3OEQLatZ4OJJk781KIQNqJZ1Q=
Address = 10.8.0.2/24
DNS = 1.1.1.1, 8.8.8.8

[Peer]
PublicKey = ra5KqfAWid/6ROiEATQ98Z9e+ZOJvRIV8VdWNEtE7Bk=
Endpoint = 212.113.101.104:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

---

## 3. 🚀 Shadowsocks 2022

```
ss://YWVzLTEyOC1nY206aGdpSU5ScVkzTlYxU1FqS3ROQ2VpZ0AyMTIuMTEzLjEwMS4xMDQ6ODQ0Mw==#VPS-Shadowsocks
```

---

## 4. 🔒 Trojan TLS

```
trojan://02be075a-1ae4-4326-ac46-d91f1695d941@212.113.101.104:8444#VPS-Trojan
```
