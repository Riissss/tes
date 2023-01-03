"""
سوف يتم كتابة السورس كود الخاص بالبوت هنا
"""
import time
from telebot import util
import db
import markup
import user
import sender
from config import (bot, botName, delay,CHANNEL, GROUP, OWNER, TOKEN)

def inline_menu():
    """
    Create inline menu for new chat
    :return: InlineKeyboardMarkup
    """
    callback = types.InlineKeyboardButton(
        text="\U00002709 New chat", callback_data="NewChat"
    )
    kenkan = types.InlineKeyboardButton(text="🔵 ᴏᴡɴᴇʀ", url=f"t.me/{OWNER}")
    group = types.InlineKeyboardButton(text="👥 ɢʀᴏᴜᴘ", url=f"https://t.me/{GROUP}")
    channel = types.InlineKeyboardButton(
        text="ᴄʜᴀɴɴᴇʟ 📣", url=f"https://t.me/{CHANNEL}"
    )
    menu = types.InlineKeyboardMarkup()
    menu.add(kenkan, channel, group, callback)

    return menu


# يلتقط الاوامر
@bot.message_handler(commands=["start", "help", "search", 
                                "new_name", "my_name", "stop",
                                    "cancel","terms_and_conditions",
                                        "privacy_policy","report"])
def command_handler(message):
    chat_id = str(message.chat.id)
    chat_is_private = message.chat.type == "private"
    text = message.text
    partner_id =  user.partner(chat_id)
    in_session = user.in_sessions(chat_id)
    username = user.username(chat_id)
    # التحقق هل المحادثة خاصة، ام في محادثة عامة
    if chat_is_private:
        if user.check_reports(message, chat_id):
            # اذا كان النص من هذول الاثنين
            if text.startswith(("/start", "/help", "/terms_and_conditions",
                                            "/privacy_policy")):
                # ازالة علامة الكوماند
                command = text[1:]
                if command in ["terms_and_conditions", "privacy_policy"]:
                    with open(command+'.txt', 'r', encoding="utf-8") as f:
                        for text in util.split_string(f.read(), 3000):
                            bot.reply_to(message, text)
                else:
                    # جلب الرسالة من قاعدة البيانات بعد ازالة ال / للبحث عنه
                    msg = db.row("message", "msg", command, "val")
                    #  ارسال الرسالة الى المستخدم
                    bot.reply_to(message, msg)
            elif text.startswith("/search"):
                # اذا كان المستخدم موجود في قاعدة البيانات
                if user.found(chat_id):
                    if not in_session:
                        if not user.waiting(chat_id):
                            if len(db.column('waiting', 'id')) != 0:
                                user.make_session(chat_id)
                            else:
                                user.add_to_waiting(chat_id)
                                msg = "[Pesan dari bot 🤖]\n\nAnda telah ditambahkan ke daftar tunggu, ketika seseorang ditemukan, pesan akan dikirimkan kepada Anda\nUntuk membatalkan, kirim /cancel"
                                bot.reply_to(message, msg)
                        else:
                            bot.reply_to(message, "[Pesan dari bot 🤖]\n\nAnda benar-benar dalam daftar tunggu\n /cancel Untuk membatalkan kirim")
                    else:
                        bot.reply_to(message, "[رسالة من البوت 🤖]\n\nانت في جلسة حقا")
                else:
                    # جلب الرسالة من قاعدة البيانات
                    msg = db.row("message", "msg", "no_user", "val")
                    #  ارسال الرسالة الى المستخدم
                    bot.reply_to(message, msg, reply_markup=markup.make_username())
            elif text.startswith("/new_name"):
                user.add_user(chat_id, not chat_id in db.column('users', 'id'))
            elif text.startswith("/my_name"):
                if username:
                    msg = "[Sebuah pesan dari bot 🤖]\n\nNama Anda saat ini adalah: %s\n\nInfo:\nNama ini akan ditampilkan kepada siapa pun yang Anda ajak chat melalui bot" % username
                else:
                    msg = "[Pesan dari bot 🤖]\n\nNama belum dibuat untuk Anda.\nUntuk membuat nama, kirim /new_name "
                bot.reply_to(message, msg)
            elif text.startswith("/cancel"):
                if user.waiting(chat_id):
                    user.del_waiting(chat_id)
                    bot.reply_to(message, "[Pesan dari bot 🤖]\n\nPencarian obrolan telah berhasil dibatalkan")
                else:
                    bot.reply_to(message, "[Pesan dari bot 🤖]\n\nAnda tidak berada dalam obrolan untuk mencari obrolan pasangan /search")
            elif text.startswith("/stop"):
                if in_session:
                    sessions_id = db.row('chat_sessions', 'user_id', chat_id, 'sessions')
                    user.delete_sessions(sessions_id, chat_id)
                    msg = "[Sebuah pesan dari bot 🤖]\n\nObrolan telah berhasil dihentikan\untuk mencari obrolan lain /search"
                    bot.reply_to(message, msg)
                else:
                    msg = "[Pesan dari bot 🤖]\n\nAnda tidak berada di obrolan yang benarا"
                    bot.reply_to(message, msg,reply_markup=menu)
            elif text.startswith("/report"):
                if in_session:
                    user.make_report(message, chat_id, username, partner_id)
                else:
                    bot.reply_to(message, "Anda tidak berada dalam obrolan\nAnda dapat melaporkan pasangan Anda dalam obrolan saat Anda berada dalam suatu obrolan")
            else:
                pass
        # اذ كان محظور سوف يتم ارسال له رسالة من داخل الدالة
        else:
            pass
    else:
        # جلب الرسالة من قاعدة البيانات
        msg = db.row("message", "msg", "not_private", "val")
        #  ارسال الرسالة الى المستخدم
        bot.reply_to(message, msg)

# يلتقط جميع الرسايل ماعدا الاوامر
@bot.message_handler(func=lambda msg: True, content_types= ["text", "audio", "document", "photo", "sticker",
                                                            "video", "video_note", "voice", "animation"])
def message_handler(message):
    chat_id = str(message.chat.id)
    # التحقق من ان الشخص ليس محظور
    if user.check_reports(message, chat_id):
        # اذا كان هناك جلسة
        if user.in_sessions(chat_id):
            partner_id =  user.partner(chat_id)
            time_now = time.time()
            # التحقق ان وقت الجلسة لم ينتهي
            if time_now < float(user.sessions_time(chat_id)):
                reply_msg_id = str(message.reply_to_message.id) if message.reply_to_message else None
                if message.text == "meninjau":
                    sender.delete(message, reply_msg_id, partner_id)
                else:
                    user_last_msg_time = float(db.row('users', "id", chat_id, "last_msg"))
                    # التحقق من وقت اخر رسالة
                    if time_now >= (user_last_msg_time+delay):
                        # تحديث وقت اخر رسالة
                        db.update("users", "last_msg", time_now, "id", chat_id)
                        # اذا تم الرد على رسالة
                        if reply_msg_id:
                            sender.reply_message(message, chat_id, reply_msg_id)
                        # اذا لم يتم الرد على رسالة
                        else:
                            sender.send_to_partner(message, chat_id)
                    else:
                        bot.reply_to(message, "[Sebuah pesan dari bot 🤖]\n\nPesan tidak berhasil terkirim, karena ketidaksesuaian dengan waktu antara setiap pesan, yaitu %s detik" % delay)
            else:
                # ايقاف الجلسة اذ انتها وقتها
                sessions_id = user.get_sessions(chat_id)
                user.kill_session(sessions_id)
                msg = "[Pesan dari bot 🤖]\n\nWaktu obrolan telah habis, untuk mencari obrolan lain /search"
                for u_id in [chat_id, partner_id]:
                        bot.send_message(u_id, msg)         
        # اذ لم يكن في جلسة، سوف يتم تجاهل الرسالة
        else:
            pass
    # اذ كان محظور سوف يتم ارسال له رسالة من داخل الدالة
    else:
        pass

@bot.edited_message_handler(func=lambda msg:True, content_types= ["text", "document", "photo",
                                                            "video", "voice", "animation"])
def edit_message_handler(message):
    chat_id = str(message.chat.id)
    msg_id = str(message.id)
    if user.found(chat_id):
        if user.in_sessions(chat_id):
            sender.edit_message(msg_id, chat_id, message)
        else:
            pass
    else:
        pass

@bot.callback_query_handler(func=lambda call:True)
def query_handler(call):
    callback = call.data
    user_id = str(call.from_user.id)
    # اذا كن الزر المضغوط هو زر اختيار الاسم
    if callback == "username":
        # اذا كان اليوزر ليس موجود في قاعدة البيانات
        if not user.found(user_id):
            user.add_user(user_id, new_user=True)
            bot.delete_message(user_id, call.message.id)
        else:
            # اخباره بأمر تحديث الاسم لان الزر فق للمستخدم الجديد
            bot.send_message(user_id, "[Pesan dari bot 🤖]\n\nUntuk memperbarui nama panggilan, kirim /new_name")
    else:
        bot.answer_callback_query(call.id, "pengirim %s" % callback)

# تشغيل البوت
while True:
    print(f"Start {botName}")
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except Exception as e:
        print(e)
        time.sleep(10)