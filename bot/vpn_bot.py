#!/usr/bin/env python3
"""
Telegram VPN Management & Config Bot (IPv6 Optimized)
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
IPV6_HOST = "2a0b:4140:e510::2"
PORTAL_URL = f"http://[{IPV6_HOST}]/"
CONFIGS_PATH = "/opt/vps_vpn/configs.json"

bot = telebot.TeleBot(TOKEN)

def load_configs():
    if os.path.exists(CONFIGS_PATH):
        with open(CONFIGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

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
    b_portal = types.KeyboardButton("🌐 Веб-Кабинет (IPv6)")
    b0 = types.KeyboardButton("📥 Единая Подписка (IPv6 Happ)")
    b1 = types.KeyboardButton("⚡ VLESS Reality (Чистый IPv6)")
    b2 = types.KeyboardButton("🛡 WireGuard (IPv6)")
    b3 = types.KeyboardButton("🚀 Shadowsocks")
    b4 = types.KeyboardButton("🌐 Админка 3X-UI")
    b5 = types.KeyboardButton("📲 Скачать клиенты")
    markup.add(b_portal)
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
        "👋 **Добро пожаловать в панель VPS VPN (IPv6 Active)!**\n\n"
        f"✨ **Чистый IPv6 адрес сервера:** `[{IPV6_HOST}]` (работает в обход блокировок ТСПУ)\n\n"
        f"🌐 **Веб-Кабинет:** [http://[{IPV6_HOST}]/](http://[{IPV6_HOST}]/)\n\n"
        "Выберите действие в меню ниже:\n"
        "• **📥 Единая Подписка (IPv6 Happ)** — ссылка автообновления для Happ / Streisand.\n"
        "• **⚡ VLESS Reality (Чистый IPv6)** — готовые профили iCloud и Microsoft.\n"
        "• **🛡 WireGuard (IPv6)** — полноканальный VPN туннель.\n"
        "• **🌐 Веб-Кабинет** — тест ТСПУ и QR-коды прямо в браузере."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_keyboard(user_id))

@bot.message_handler(func=lambda msg: msg.text == "🌐 Веб-Кабинет (IPv6)")
def handle_portal_link(message):
    text = (
        "🌐 **Веб-Кабинет и Центр Диагностики ТСПУ (IPv6)**\n\n"
        f"🔗 **Ссылка для входа:** {PORTAL_URL}\n\n"
        "Откройте ссылку с телефона в мобильной сети (МТС, Билайн, Мегафон, Теле2)."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "📥 Единая Подписка (IPv6 Happ)")
def handle_subscription(message):
    sub_url = f"http://[{IPV6_HOST}]:2096/9k7xuvoxldiq5zsh/0861ace1ba5cd059"
    caption = (
        "📥 **Единая ссылка подписки (IPv6 Автообновление)**\n\n"
        "Нажмите на ссылку, чтобы скопировать её:\n"
        f"`{sub_url}`\n\n"
        "📱 **Как добавить в Happ / Streisand / v2rayNG:**\n"
        "1. Скопируйте ссылку выше (или отсканируйте QR-код).\n"
        "2. Откройте **Happ** -> нажмите **`+`** -> **Добавить подписку** (Импорт).\n"
        "3. В списке появятся серверы — выберите и нажмите **Подключиться**."
    )
    qr_img = make_qr_code(sub_url)
    bot.send_photo(message.chat.id, qr_img, caption=caption, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "⚡ VLESS Reality (Чистый IPv6)")
def handle_vless_configs(message):
    client_uuid = "8cb32046-0d00-40c6-81c0-325bc1ac8fa4"
    pbk = "g6pfxKCDQFLpN1BKaSC-to-_orpUlP7WyiE9ATAfUxs"
    sid = "106ec6b5"
    
    vless_icloud = f"vless://{client_uuid}@[{IPV6_HOST}]:443?type=tcp&security=reality&pbk={pbk}&fp=chrome&sni=gateway.icloud.com&sid={sid}&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20VPS%20%E2%9A%A1%20IPv6%20Reality%20(iCloud)"
    vless_ms = f"vless://{client_uuid}@[{IPV6_HOST}]:443?type=tcp&security=reality&pbk={pbk}&fp=chrome&sni=www.microsoft.com&sid={sid}&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20VPS%20%E2%9A%A1%20IPv6%20Reality%20(Microsoft)"

    caption = (
        "⚡ **VLESS Reality (Чистый IPv6 — Обход ТСПУ)**\n\n"
        "🔹 **1. Apple iCloud Gateway (Основной / Эталонный):**\n"
        f"`{vless_icloud}`\n\n"
        "🔹 **2. Microsoft SNI:**\n"
        f"`{vless_ms}`\n\n"
        "📲 *Скопируйте ссылку выше и вставьте в Happ / Streisand / v2ray.*"
    )
    qr_img = make_qr_code(vless_icloud)
    bot.send_photo(message.chat.id, qr_img, caption=caption, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "🛡 WireGuard (IPv6)")
def handle_wireguard(message):
    cfg = load_configs()
    wg_conf = cfg.get("wg_client_conf", "")
    caption = (
        "🛡 **WireGuard VPN Конфигурация (IPv6)**\n\n"
        f"Endpoint: `[{IPV6_HOST}]:51820`\n"
        "Отсканируйте QR-код в приложении **WireGuard** или используйте файл ниже."
    )
    qr_img = make_qr_code(wg_conf)
    bot.send_photo(message.chat.id, qr_img, caption=caption, parse_mode="Markdown")
    
    conf_file = io.BytesIO(wg_conf.encode('utf-8'))
    conf_file.name = "vps_vpn_ipv6.conf"
    bot.send_document(message.chat.id, conf_file, caption="📄 Файл конфигурации WireGuard (IPv6)")

@bot.message_handler(func=lambda msg: msg.text == "🚀 Shadowsocks")
def handle_shadowsocks(message):
    ss_raw = "aes-128-gcm:zupWFBehJidNA1y5KbsvbA@" + f"[{IPV6_HOST}]:8443"
    import base64
    ss_b64 = base64.urlsafe_b64encode(ss_raw.encode()).decode()
    ss_link = f"ss://{ss_b64}#VPS-IPv6-Shadowsocks"
    caption = f"🚀 **Shadowsocks 2022 (IPv6)**\n\n`{ss_link}`"
    qr_img = make_qr_code(ss_link)
    bot.send_photo(message.chat.id, qr_img, caption=caption, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "🌐 Админка 3X-UI")
def handle_admin_panel(message):
    text = (
        "🌐 **Веб-панель 3X-UI (IPv6)**\n\n"
        f"🔗 **URL:** `http://[{IPV6_HOST}]:2053/D11nS5my7qbNKjqt7L/`\n"
        "👤 **Логин:** `admin`\n"
        "🔑 **Пароль:** `AdminVpn2026!`"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "📲 Скачать клиенты")
def handle_clients(message):
    text = (
        "📲 **Рекомендуемые клиенты для подключения:**\n\n"
        "🍏 **iOS / iPad / macOS:**\n"
        "• [Happ (Рекомендуется)](https://apps.apple.com/app/happ-proxy-utility/id6504287215)\n"
        "• [Streisand](https://apps.apple.com/app/streisand/id6450534064)\n"
        "• [WireGuard](https://apps.apple.com/app/wireguard/id1441195209)\n\n"
        "🤖 **Android:**\n"
        "• [Happ (Google Play)](https://play.google.com/store/apps/details?id=com.happproxy)\n"
        "• [v2rayNG](https://github.com/2dust/v2rayNG/releases)\n"
        "• [WireGuard](https://play.google.com/store/apps/details?id=com.wireguard.android)"
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
        bbr = subprocess.getoutput("sysctl -n net.ipv4.tcp_congestion_control")
        xui = subprocess.getoutput("systemctl is-active x-ui")
        wg = subprocess.getoutput("systemctl is-active wg-quick@wg0")
        portal = subprocess.getoutput("systemctl is-active vps-vpn-portal")
        
        status_msg = (
            f"📊 **Статус Сервера (IPv6: [{IPV6_HOST}])**\n\n"
            f"⏱ **Аптайм:** `{uptime}`\n"
            f"🚀 **TCP BBR:** `{bbr}`\n"
            f"🔹 **3X-UI Service:** `{xui}`\n"
            f"🔹 **WireGuard Service:** `{wg}`\n"
            f"🔹 **Web Portal Service:** `{portal}`\n\n"
            f"🧠 **Память:**\n```\n{mem}\n```\n"
            f"💾 **Диск:**\n```\n{disk}\n```"
        )
        bot.send_message(call.message.chat.id, status_msg, parse_mode="Markdown")

    elif data == "adm_restart_xui":
        res = subprocess.getoutput("systemctl restart x-ui")
        bot.send_message(call.message.chat.id, "✅ Служба 3X-UI перезапущена!", parse_mode="Markdown")

    elif data == "adm_restart_wg":
        res = subprocess.getoutput("systemctl restart wg-quick@wg0")
        bot.send_message(call.message.chat.id, "✅ Служба WireGuard перезапущена!", parse_mode="Markdown")

    elif data == "adm_ufw":
        ufw = subprocess.getoutput("ufw status verbose")
        bot.send_message(call.message.chat.id, f"🛡 **Статус Фаервола UFW:**\n```\n{ufw}\n```", parse_mode="Markdown")

if __name__ == "__main__":
    print(f"Starting VPN Telegram Bot (Admin: {ADMIN_ID})...")
    bot.infinity_polling()
