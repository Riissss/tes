from .markup_config import MARKUP, BUTTON

def make_username():
    markup = MARKUP()
    markup.add(
        BUTTON(text="Klik di sini untuk memasukkan nama", callback_data="username")
    )
    return markup