import db
from config import bot, max_reports

def check_reports(message, user_id):
    
    user_reports = db.row('users', "id", user_id, "reports")
    if user_reports:
        if int(user_reports) < max_reports:
            return True
        else:
            bot.reply_to(message, "Anda telah mencapai batas pesan, yaitu %s, jumlah pesan yang Anda miliki adalah %s\n\nBatas pesan menjaga bot tetap stabil" % (max_reports, user_reports))
            return False
    else:
        return True