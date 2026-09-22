# 📱 Готовые конфигурации и Подписка (Client Configs)

Сервер: **`v3.idivles.ru`** (IP: `212.113.101.104`)

---

## 🌐 0. Интерактивный Веб-Кабинет & Диагностика ТСПУ

> 🔗 **Адрес портала:** **[http://v3.idivles.ru:8080](http://v3.idivles.ru:8080)**  
> Проверяет блокировки ТСПУ оператора, тест доступности портов, пинг и генерирует QR-коды для сканирования с экрана.

## 📥 1. Единая ссылка подписки (Рекомендуется для Happ / Streisand / v2ray)

> **Преимущество:** Добавляется один раз в приложение. При любых изменениях на сервере клиент автоматически обновляет список серверов и протоколов.

```
https://v3.idivles.ru:2096/9k7xuvoxldiq5zsh/0861ace1ba5cd059
```

### 📱 Инструкция для Happ (iOS / Android):
1. Скопируйте ссылку подписки выше.
2. Откройте приложение **Happ** (или Streisand / v2rayNG / v2rayN / Hiddify).
3. Нажмите **+** -> **Добавить подписку (Импорт из буфера обмена)**.
4. Выберите нужный сервер из списка и нажмите **Подключиться**.

---

## ⚡ 2. Популярные конфигурации VLESS Reality (Прямой импорт)

### 🔹 Google SNI (Основной, маскировка под Google Chrome / Downloads):
```
vless://8cb32046-0d00-40c6-81c0-325bc1ac8fa4@v3.idivles.ru:443?type=tcp&security=reality&pbk=g6pfxKCDQFLpN1BKaSC-to-_orpUlP7WyiE9ATAfUxs&fp=chrome&sni=dl.google.com&sid=106ec6b5&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20VPS%20%E2%9A%A1%20VLESS%20Reality%20(Google)
```

### 🔹 Microsoft SNI (Повышенная проходимость через ТСПУ / DPI):
```
vless://8cb32046-0d00-40c6-81c0-325bc1ac8fa4@v3.idivles.ru:443?type=tcp&security=reality&pbk=g6pfxKCDQFLpN1BKaSC-to-_orpUlP7WyiE9ATAfUxs&fp=chrome&sni=www.microsoft.com&sid=106ec6b5&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20VPS%20%E2%9A%A1%20VLESS%20Reality%20(Microsoft)
```

### 🔹 Samsung SNI:
```
vless://8cb32046-0d00-40c6-81c0-325bc1ac8fa4@v3.idivles.ru:443?type=tcp&security=reality&pbk=g6pfxKCDQFLpN1BKaSC-to-_orpUlP7WyiE9ATAfUxs&fp=chrome&sni=www.samsung.com&sid=106ec6b5&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20VPS%20%E2%9A%A1%20VLESS%20Reality%20(Samsung)
```

### 🔹 Direct IP (для сетей без доступа к DNS):
```
vless://8cb32046-0d00-40c6-81c0-325bc1ac8fa4@212.113.101.104:443?type=tcp&security=reality&pbk=g6pfxKCDQFLpN1BKaSC-to-_orpUlP7WyiE9ATAfUxs&fp=chrome&sni=dl.google.com&sid=106ec6b5&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20VPS%20%E2%9A%A1%20Direct%20IP%20(Google)
```

---

## 🛡 3. WireGuard (Полноканальный VPN)

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

## 🚀 4. Shadowsocks 2022

```
ss://YWVzLTEyOC1nY206enVwV0ZCZWhKaWROQTF5NUtic3ZiQUB2My5pZGl2bGVzLnJ1Ojg0NDM=#VPS-Shadowsocks
```

---

## 🔒 5. Trojan TLS (Let's Encrypt SSL)

```
trojan://cd3a13d7-46fe-40d4-904b-e522fe459544@v3.idivles.ru:8444?security=tls&sni=v3.idivles.ru#VPS-Trojan-TLS
```

---

## 🌐 6. Веб-Панель управления 3X-UI

- **URL:** [https://v3.idivles.ru:2053/D11nS5my7qbNKjqt7L/](https://v3.idivles.ru:2053/D11nS5my7qbNKjqt7L/)
- **Логин:** `admin`
- **Пароль:** `AdminVpn2026!`
