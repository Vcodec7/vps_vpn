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
        "vless_link": "vless://f3923284-03eb-4920-839a-9195af363bca@212.113.101.104:443?type=tcp&security=reality&pbk=8umwn2l_7CTOfHkc9eIzLW-alojT5Nlrpi0Aa_ssmGY&fp=chrome&sni=dl.google.com&sid=2a7136af&flow=xtls-rprx-vision#VPS-VLESS-Reality",
        "ss_link": "ss://YWVzLTEyOC1nY206aGdpSU5ScVkzTlYxU1FqS3ROQ2VpZ0AyMTIuMTEzLjEwMS4xMDQ6ODQ0Mw==#VPS-Shadowsocks",
        "trojan_link": "trojan://02be075a-1ae4-4326-ac46-d91f1695d941@212.113.101.104:8444#VPS-Trojan",
        "wg_client_conf": "[Interface]\nPrivateKey = cP9PCbdWcKGi0wg8Zq3OEQLatZ4OJJk781KIQNqJZ1Q=\nAddress = 10.8.0.2/24\nDNS = 1.1.1.1, 8.8.8.8\n\n[Peer]\nPublicKey = ra5KqfAWid/6ROiEATQ98Z9e+ZOJvRIV8VdWNEtE7Bk=\nEndpoint = 212.113.101.104:51820\nAllowedIPs = 0.0.0.0/0, ::/0\nPersistentKeepalive = 25\n",
        "admin_panel": {
            "url": "http://212.113.101.104:18550/D11nS5my7qbNKjqt7L/",
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
    b1 = types.KeyboardButton("⚡ VLESS Reality")
    b2 = types.KeyboardButton("🛡 WireGuard")
    b3 = types.KeyboardButton("🚀 Shadowsocks")
    b4 = types.KeyboardButton("🌐 Веб-Админка 3X-UI")
    b5 = types.KeyboardButton("📲 Скачать клиенты")
    markup.add(b1, b2, b3, b4, b5)
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
    b5 = types.InlineKeyboardButton("🔑 Новые ключи VLESS", callback_data="adm_gen_vless")
    markup.add(b1, b2, b3, b4, b5)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    cfg = load_configs()
    welcome_text = (
        "👋 **Добро пожаловать в панель управления VPS VPN!**\n\n"
        "Выберите протокол для получения конфигурации или QR-кода:\n\n"
        "• **⚡ VLESS Reality** — самый надежный и устойчивый к любым блокировкам (маскировка под Google).\n"
        "• **🛡 WireGuard** — быстрый полноканальный VPN для ПК и телефонов.\n"
        "• **🚀 Shadowsocks 2022** — быстрый легкий прокси-туннель.\n"
        "• **🌐 Веб-Админка 3X-UI** — веб-интерфейс создания пользователей и мониторинга.\n"
        "• **📲 Скачать клиенты** — ссылки на проверенные приложения."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_keyboard(user_id))

@bot.message_handler(func=lambda msg: msg.text == "⚡ VLESS Reality")
def handle_vless(message):
    cfg = load_configs()
    vless_link = cfg.get("vless_link", "")
    caption = (
        "⚡ **VLESS + XTLS-Reality (Рекомендуемый)**\n\n"
        "Нажмите на ссылку, чтобы скопировать её:\n"
        f"`{vless_link}`\n\n"
        "📖 **Как подключиться:**\n"
        "1. Скопируйте ссылку выше или отсканируйте QR-код.\n"
        "2. Откройте приложение (**Happ**, **Streisand**, **v2rayNG**, **NekoBox**, **v2rayN**).\n"
        "3. Нажмите **+** -> **Импорт из буфера обмена** (или скан QR)."
    )
    qr_img = make_qr_code(vless_link)
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
    bot.send_document(message.chat.id, conf_file, caption="📄 Файл конфигурации для WireGuard клиента")

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
    cfg = load_configs()
    panel = cfg.get("admin_panel", {})
    text = (
        "🌐 **Веб-панель управления 3X-UI (Xray Core)**\n\n"
        f"🔗 **URL:** `{panel.get('url')}`\n"
        f"👤 **Логин:** `{panel.get('username')}`\n"
        f"🔑 **Пароль:** `{panel.get('password')}`\n\n"
        "💡 В панели можно создавать новых клиентов с ограничением по трафику, настраивать порты и смотреть статистику."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "📲 Скачать клиенты")
def handle_clients(message):
    text = (
        "📲 **Рекомендуемые клиенты для подключения:**\n\n"
        "🍏 **iOS / iPad / macOS:**\n"
        "• [Happ](https://apps.apple.com/app/happ-proxy-utility/id6504287215) (VLESS Reality)\n"
        "• [Streisand](https://apps.apple.com/app/streisand/id6450534064) (VLESS Reality)\n"
        "• [FoXray](https://apps.apple.com/app/foxray/id6448898396)\n"
        "• [WireGuard](https://apps.apple.com/app/wireguard/id1441195209)\n\n"
        "🤖 **Android:**\n"
        "• [Happ](https://play.google.com/store/apps/details?id=com.happproxy)\n"
        "• [v2rayNG](https://github.com/2dust/v2rayNG/releases)\n"
        "• [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases)\n"
        "• [WireGuard](https://play.google.com/store/apps/details?id=com.wireguard.android)\n\n"
        "💻 **Windows / macOS / Linux:**\n"
        "• [v2rayN (Windows)](https://github.com/2dust/v2rayN/releases)\n"
        "• [Hiddify (Все платформы)](https://github.com/hiddify/hiddify-next/releases)\n"
        "• [Nekoray (Windows/Linux)](https://github.com/MatsuriDayo/nekoray/releases)\n"
        "• [WireGuard Desktop](https://www.wireguard.com/install/)"
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
            f"📊 **Статус Сервера 212.113.101.104**\n\n"
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
        bot.send_message(call.message.chat.id, "🔄 Генерация нового VLESS-ключа...")
        subprocess.getoutput("python3 /tmp/setup_protocols.py")
        cfg = load_configs()
        vless_link = cfg.get("vless_link", "")
        qr_img = make_qr_code(vless_link)
        bot.send_photo(call.message.chat.id, qr_img, caption=f"✅ Новый VLESS ключ:\n`{vless_link}`", parse_mode="Markdown")

if __name__ == "__main__":
    print(f"Starting VPN Telegram Bot (Admin: {ADMIN_ID})...")
    bot.infinity_polling()
