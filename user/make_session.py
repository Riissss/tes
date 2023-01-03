import db
from config import  bot, session_time
from .username import username
from .del_waiting import del_waiting
from random import choice
from time import time
from pytz import UTC
from datetime import datetime

def make_session(user_id):
    """ انشاء جلسة بين اثنين

    المتغيرات:
        user_id (str): الايدي الخاص بالشخص المراد بحث جلسة له
    """
    # اذا تم العثور على منتظرين
    if len(db.column('waiting', 'id')) > 0:
        user_id2 = choice(db.column('waiting', 'id'))
        session_id = user_id+user_id2
        end_time = time()+session_time
        end_date = str(datetime.fromtimestamp(end_time, UTC).strftime("%I:%M %p %Z"))
        del_waiting(user_id2)
        for user in [user_id, user_id2]:
            db.insert('chat_sessions', (session_id, user, end_time))
            bot.send_message(user, "Obrolan telah dibuat dengan %s\nUntuk menyela sesi, kirim /bunuh\n\nObrolan akan disela di \n%s\nPercakapan yang menarik 🌹" % (username(user_id if user_id != user else user_id2), end_date))
    # الغاء انشاء جلسة
    else:
        pass