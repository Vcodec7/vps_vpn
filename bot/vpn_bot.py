#!/usr/bin/env python3
"""
Telegram VPN Management & Config Bot
Token: 8626856754:AAGqy454SZaLuZ4ftY7yrRIf57nnv5eozbI
Admin ID: 8555955292
"""

import os
import sys
import json
import io
import subprocess
import qrcode
from PIL import Image
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN", "8626856754:AAGqy454SZaLuZ4ftY7yrRIf57nnv5eozbI")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8555955292"))
CONFIGS_PATH = "/opt/vps_vpn/configs.json"

bot = telebot.TeleBot(TOKEN)

def load_configs():
    if os.path.exists(CONFIGS_PATH):
        with open(CONFIGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "domain": "v3.idivles.ru",
        "sub_url": "https://v3.idivles.ru:2096/9k7xuvoxldiq5zsh/0861ace1ba5cd059",
        "vless_link": "vless://8cb32046-0d00-40c6-81c0-325bc1ac8fa4@v3.idivles.ru:443?type=tcp&security=reality&pbk=g6pfxKCDQFLpN1BKaSC-to-_orpUlP7WyiE9ATAfUxs&fp=chrome&sni=dl.google.com&sid=106ec6b5&flow=xtls-rprx-vision#VPS-VLESS-Reality",
        "ss_link": "ss://YWVzLTEyOC1nY206enVwV0ZCZWhKaWROQTF5NUtic3ZiQUB2My5pZGl2bGVzLnJ1Ojg0NDM=#VPS-Shadowsocks",
        "trojan_link": "trojan://cd3a13d7-46fe-40d4-904b-e522fe459544@v3.idivles.ru:8444?security=tls&sni=v3.idivles.ru#VPS-Trojan-TLS",
        "wg_client_conf": "[Interface]\nPrivateKey = SLcXGBmkqtmxAoTW6d0wd56XHAD29XWm/GNqaTmefm8=\nAddress = 10.8.0.2/24\nDNS = 1.1.1.1, 8.8.8.8\n\n[Peer]\nPublicKey = ulrgbD+6G59BqcnRJDL357A1xMAQ8oBti/55BrjoNB4=\nEndpoint = v3.idivles.ru:51820\nAllowedIPs = 0.0.0.0/0, ::/0\nPersistentKeepalive = 25\n",
        "admin_panel": {
            "url": "https://v3.idivles.ru:2053/D11nS5my7qbNKjqt7L/",
            "username": "admin",
            "password": "AdminVpn2026!"
        }
    }

def make_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=3,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    bio = io.BytesIO()
    bio.name = 'qrcode.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    return bio

def main_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    b0 = types.KeyboardButton("📥 Единая Подписка (Happ / iOS / Android)")
    b1 = types.KeyboardButton("⚡ Популярные VLESS Конфиги")
    b2 = types.KeyboardButton("🛡 WireGuard")
    b3 = types.KeyboardButton("🚀 Shadowsocks")
    b4 = types.KeyboardButton("🌐 Веб-Админка 3X-UI")
    b5 = types.KeyboardButton("📲 Скачать клиенты (Happ / v2ray)")
    markup.add(b0)
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(b5)
    if user_id == ADMIN_ID:
        b_admin = types.KeyboardButton("⚙️ Админ-панель VPS")
        markup.add(b_admin)
    return markup

def admin_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("📊 Статус сервера", callback_data="adm_status")
    b2 = types.InlineKeyboardButton("🔄 Рестарт Xray / 3X-UI", callback_data="adm_restart_xui")
    b3 = types.InlineKeyboardButton("🔄 Рестарт WireGuard", callback_data="adm_restart_wg")
    b4 = types.InlineKeyboardButton("🛡 Статус UFW", callback_data="adm_ufw")
    b5 = types.InlineKeyboardButton("🔑 Сгенерировать ключи", callback_data="adm_gen_vless")
    markup.add(b1, b2, b3, b4, b5)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    welcome_text = (
        "👋 **Добро пожаловать в панель управления VPS VPN!**\n\n"
        "✨ **Сервер:** `v3.idivles.ru` (Все протоколы активны)\n\n"
        "Выберите нужное действие в меню ниже:\n"
        "• **📥 Единая Подписка** — одна ссылка для всех профилей с автообновлением в **Happ** / **Streisand** / **v2ray**.\n"
        "• **⚡ Популярные VLESS Конфиги** — готовые ссылки с маскировкой (Google, Microsoft, Samsung).\n"
        "• **🛡 WireGuard** — файл `.conf` и QR-код для классического VPN.\n"
        "• **🚀 Shadowsocks** — быстрый прокси-туннель.\n"
        "• **🌐 Веб-Админка 3X-UI** — управление клиентами через защищенный HTTPS."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_keyboard(user_id))

@bot.message_handler(func=lambda msg: msg.text == "📥 Единая Подписка (Happ / iOS / Android)")
def handle_subscription(message):
    sub_url = "https://v3.idivles.ru:2096/9k7xuvoxldiq5zsh/0861ace1ba5cd059"
    caption = (
        "📥 **Единая ссылка подписки (Автообновление)**\n\n"
        "Нажмите на ссылку, чтобы скопировать её:\n"
        f"`{sub_url}`\n\n"
        "📱 **Как добавить в Happ (iOS / Android):**\n"
        "1. Скопируйте ссылку выше (или отсканируйте QR-код).\n"
        "2. Откройте приложение **Happ** (или Streisand / v2rayNG / v2rayN / Hiddify).\n"
        "3. Нажмите **+** в правом верхнем углу -> **Добавить подписку** (Import from clipboard).\n"
        "4. Все серверы и протоколы сразу загрузятся в список!\n\n"
        "💡 *При обновлении конфигураций на сервере клиент будет подтягивать их автоматически.*"
    )
    qr_img = make_qr_code(sub_url)
    bot.send_photo(message.chat.id, qr_img, caption=caption, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text in ["⚡ Популярные VLESS Конфиги", "⚡ VLESS Reality"])
def handle_vless_configs(message):
    # Основные маскировки VLESS Reality
    vless_google = "vless://8cb32046-0d00-40c6-81c0-325bc1ac8fa4@v3.idivles.ru:443?type=tcp&security=reality&pbk=g6pfxKCDQFLpN1BKaSC-to-_orpUlP7WyiE9ATAfUxs&fp=chrome&sni=dl.google.com&sid=106ec6b5&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20VPS%20%E2%9A%A1%20VLESS%20Reality%20(Google)"
    vless_ms = "vless://8cb32046-0d00-40c6-81c0-325bc1ac8fa4@v3.idivles.ru:443?type=tcp&security=reality&pbk=g6pfxKCDQFLpN1BKaSC-to-_orpUlP7WyiE9ATAfUxs&fp=chrome&sni=www.microsoft.com&sid=106ec6b5&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20VPS%20%E2%9A%A1%20VLESS%20Reality%20(Microsoft)"
    vless_samsung = "vless://8cb32046-0d00-40c6-81c0-325bc1ac8fa4@v3.idivles.ru:443?type=tcp&security=reality&pbk=g6pfxKCDQFLpN1BKaSC-to-_orpUlP7WyiE9ATAfUxs&fp=chrome&sni=www.samsung.com&sid=106ec6b5&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20VPS%20%E2%9A%A1%20VLESS%20Reality%20(Samsung)"
    vless_ip = "vless://8cb32046-0d00-40c6-81c0-325bc1ac8fa4@212.113.101.104:443?type=tcp&security=reality&pbk=g6pfxKCDQFLpN1BKaSC-to-_orpUlP7WyiE9ATAfUxs&fp=chrome&sni=dl.google.com&sid=106ec6b5&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20VPS%20%E2%9A%A1%20Direct%20IP%20(Google)"

    caption = (
        "⚡ **Популярные конфигурации VLESS Reality**\n\n"
        "🔹 **1. Google SNI (Основной / Быстрый):**\n"
        f"`{vless_google}`\n\n"
        "🔹 **2. Microsoft SNI (Максимальный обход блокировок):**\n"
        f"`{vless_ms}`\n\n"
        "🔹 **3. Samsung SNI:**\n"
        f"`{vless_samsung}`\n\n"
        "🔹 **4. Прямой IP (без DNS):**\n"
        f"`{vless_ip}`\n\n"
        "📲 *Нажмите на любую ссылку выше, чтобы скопировать и вставить в Happ / Streisand / v2ray.*"
    )
    qr_img = make_qr_code(vless_google)
    bot.send_photo(message.chat.id, qr_img, caption=caption, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "🛡 WireGuard")
def handle_wireguard(message):
    cfg = load_configs()
    wg_conf = cfg.get("wg_client_conf", "")
    caption = (
        "🛡 **WireGuard VPN Конфигурация**\n\n"
        "Отсканируйте QR-код в приложении **WireGuard** / **AmneziaVPN** или используйте файл конфигурации ниже."
    )
    qr_img = make_qr_code(wg_conf)
    bot.send_photo(message.chat.id, qr_img, caption=caption, parse_mode="Markdown")
    
    conf_file = io.BytesIO(wg_conf.encode('utf-8'))
    conf_file.name = "vps_vpn_client.conf"
    bot.send_document(message.chat.id, conf_file, caption="📄 Файл конфигурации для WireGuard")

@bot.message_handler(func=lambda msg: msg.text == "🚀 Shadowsocks")
def handle_shadowsocks(message):
    cfg = load_configs()
    ss_link = cfg.get("ss_link", "")
    caption = (
        "🚀 **Shadowsocks 2022 (AES-128-GCM)**\n\n"
        f"`{ss_link}`\n\n"
        "Импортируйте ссылку или QR-код в приложение **Shadowrocket**, **NekoBox**, **v2rayN**."
    )
    qr_img = make_qr_code(ss_link)
    bot.send_photo(message.chat.id, qr_img, caption=caption, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "🌐 Веб-Админка 3X-UI")
def handle_admin_panel(message):
    text = (
        "🌐 **Веб-панель управления 3X-UI (HTTPS + SSL)**\n\n"
        "🔗 **URL:** `https://v3.idivles.ru:2053/D11nS5my7qbNKjqt7L/`\n"
        "👤 **Логин:** `admin`\n"
        "🔑 **Пароль:** `AdminVpn2026!`\n\n"
        "💡 В панели можно создавать новых клиентов с ограничением по трафику, настраивать порты и смотреть статистику."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text in ["📲 Скачать клиенты (Happ / v2ray)", "📲 Скачать клиенты"])
def handle_clients(message):
    text = (
        "📲 **Рекомендуемые клиенты для подключения:**\n\n"
        "🍏 **iOS / iPad / macOS:**\n"
        "• [Happ (Рекомендуется для VLESS)](https://apps.apple.com/app/happ-proxy-utility/id6504287215)\n"
        "• [Streisand](https://apps.apple.com/app/streisand/id6450534064)\n"
        "• [FoXray](https://apps.apple.com/app/foxray/id6448898396)\n"
        "• [WireGuard](https://apps.apple.com/app/wireguard/id1441195209)\n\n"
        "🤖 **Android:**\n"
        "• [Happ (Google Play)](https://play.google.com/store/apps/details?id=com.happproxy)\n"
        "• [v2rayNG (GitHub)](https://github.com/2dust/v2rayNG/releases)\n"
        "• [v2rayTun](https://play.google.com/store/apps/details?id=com.v2raytun.android)\n"
        "• [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases)\n"
        "• [WireGuard](https://play.google.com/store/apps/details?id=com.wireguard.android)\n\n"
        "💻 **Windows / macOS / Linux:**\n"
        "• [v2rayN (Windows)](https://github.com/2dust/v2rayN/releases)\n"
        "• [Hiddify (Все платформы)](https://github.com/hiddify/hiddify-next/releases)\n"
        "• [Nekoray](https://github.com/MatsuriDayo/nekoray/releases)"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", disable_web_page_preview=True)

@bot.message_handler(func=lambda msg: msg.text == "⚙️ Админ-панель VPS")
def handle_admin_menu(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "⛔ У вас нет прав администратора.")
        return
    bot.send_message(message.chat.id, "⚙️ **Панель управления VPS:**", parse_mode="Markdown", reply_markup=admin_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith("adm_"))
def handle_admin_callback(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Доступ запрещен.")
        return

    data = call.data
    bot.answer_callback_query(call.id, "Выполняю команду...")

    if data == "adm_status":
        uptime = subprocess.getoutput("uptime -p")
        mem = subprocess.getoutput("free -h")
        disk = subprocess.getoutput("df -hT /")
        bbr = subprocess.getoutput("sysctl net.ipv4.tcp_congestion_control")
        xui = subprocess.getoutput("systemctl is-active x-ui")
        wg = subprocess.getoutput("systemctl is-active wg-quick@wg0")
        
        status_msg = (
            f"📊 **Статус Сервера v3.idivles.ru**\n\n"
            f"⏱ **Аптайм:** `{uptime}`\n"
            f"🚀 **TCP BBR:** `{bbr}`\n"
            f"🔹 **3X-UI Service:** `{xui}`\n"
            f"🔹 **WireGuard Service:** `{wg}`\n\n"
            f"🧠 **Память:**\n```\n{mem}\n```\n"
            f"💾 **Диск:**\n```\n{disk}\n```"
        )
        bot.send_message(call.message.chat.id, status_msg, parse_mode="Markdown")

    elif data == "adm_restart_xui":
        res = subprocess.getoutput("systemctl restart x-ui")
        bot.send_message(call.message.chat.id, f"✅ Служба 3X-UI перезапущена!\n`{res}`", parse_mode="Markdown")

    elif data == "adm_restart_wg":
        res = subprocess.getoutput("systemctl restart wg-quick@wg0")
        bot.send_message(call.message.chat.id, f"✅ Служба WireGuard перезапущена!\n`{res}`", parse_mode="Markdown")

    elif data == "adm_ufw":
        ufw = subprocess.getoutput("ufw status verbose")
        bot.send_message(call.message.chat.id, f"🛡 **Статус Фаервола UFW:**\n```\n{ufw}\n```", parse_mode="Markdown")

    elif data == "adm_gen_vless":
        bot.send_message(call.message.chat.id, "🔄 Перегенерация ключей...")
        subprocess.getoutput("python3 /tmp/fix_clients.py")
        bot.send_message(call.message.chat.id, "✅ Клиентские профили обновлены!")

if __name__ == "__main__":
    print(f"Starting VPN Telegram Bot (Admin: {ADMIN_ID})...")
    bot.infinity_polling()
