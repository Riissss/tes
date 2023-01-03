import user, db
from config import bot
from telebot.types import Message

def delete(message:Message, reply_msg_id:str, partner_id:str):
    """ مسح الرسالة من الجلسة

    Args:
        message (Message): رسالة امر المسح
        reply_msg_id (str): ايدي الرسالة المراد مسحها
        partner_id (str): ايدي الشريك في الجلسة
    """
    msg_id, chat_id = list(map(str, [message.id,message.chat.id])) # جعلهم نص
    if reply_msg_id:
        # اخذ ايدي الرسلة عند شريك الجلسة لحذفها
        partner_msg_id = user.partner_msg_id(chat_id, reply_msg_id)
        # اذا كانت الرسالة من المرسل، وفي الجلسة
        if bool(list(filter(lambda m_id: m_id == reply_msg_id, 
                                db.row("sessions_messages", "user_id", chat_id, "msg_id")))):
            for message_be_delete in [(partner_id, partner_msg_id),
                                        (chat_id, msg_id),
                                            (chat_id, reply_msg_id)]:
                try:
                    c_id, m_id = message_be_delete
                    bot.delete_message(c_id, m_id)
                except Exception:
                    pass
        else:
            bot.reply_to(message, "[pesan dari bot 🤖]\n\nUntuk pesan yang tidak ada dalam obrolan atau bukan milik Anda")
    else:
        bot.reply_to(message, "[Pesan dari bot 🤖]\n\nAnda harus mengganti pesan yang ingin Anda hapus dari pihak kedua")
