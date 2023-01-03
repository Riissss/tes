"""
انشاء قاعدة بيانات
"""
from db import make, insert

if __name__ == '__main__':
    make()
    insert(table_name='message', args=("start", "Hai!,Selamat datang di Anonymous Random Chat Public\nGunakan bot ini dengan bijak!!!\nketik /help untuk mengetahui fitur di bot kami\nJoin Group kami : https://t.me/anony_caripacar"))
    insert(table_name='message', args=("help", "Hallo, fitur dibot kami:\n/search => Mencari Pasangan\n/new_name => anda dapat mengubah nama panggilan baru\n/my_name => melihatkan nama anda\nreport => hapus pesan obrolan\n/stop => anda akan mengakhiri obrolan pasangan\n/cancel => mengakhiri"))
    insert(table_name='message', args=("no_user", "Maaf, mohon untuk menerapkan nama panggilan!\n ketik /new_name"))
    insert(table_name='message', args=("not_private", "Maaf, untuk melindungi privasi pengguna, tidak mungkin membuat sesi di obrolan publik"))
  