"""
عبر هذا الملف يتم ملئ المعلومات الاساسية
https://t.me/BotFather يمكنك جلب التوكن الخاص بالبوت عبر هذا البوت
"""

VERSION = "v2.2.1"

# ضع توكن البوت هنا
TOKEN = str("5809941857:AAGTRv-r7Ym60UGTGgsAUZSGa5x8NTXGKG8")
OWNER = os.environ.get("OWNER", "kang_culiknew") # jangan dirubah agar tidak error
GROUP = os.environ.get("GROUP", "") # 
CHANNEL = os.environ.get("CHANNEL", "vvslh_pro") # 


# وضع الفرق بين كل رسالة ورسالة اخرى
delay = 1 # 1s

# اختيار عدد البلاغات الازمة لحظر العضو
max_reports = 50 # 50

# اختار اقصى مدة للجلسة
session_time = 60*30 # 30m

# لسهولة استعمال المتغيرات بين الملفات
import telebot
bot = telebot.TeleBot(TOKEN)
botName = bot.get_me().first_name