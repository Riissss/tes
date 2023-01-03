from config import bot
from .username import username
from .partner import partner
from .kill_session import kill_session

def delete_sessions(session_id:str, user_id:str):
    """ مسح جلسة

    المتغيرات:
        session_id (str): ايدي الجلسة
        user_id (str): ايدي من قام بقطع الجلسة
    """
    partenet_id = partner(user_id)
    killer_username = username(user_id)
    kill_session(session_id)
    bot.send_message(partenet_id, "Obrolan telah ditutup oleh %s\n\n untuk mencari obrolan baru /search" % killer_username)
