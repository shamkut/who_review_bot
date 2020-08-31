from telebot import types


def create_callback_button(btn_data={}):
    keyboard = types.InlineKeyboardMarkup()
    for k, v in btn_data.items():
        btn = types.InlineKeyboardButton(text=k, callback_data=v)
        keyboard.add(btn)
    return keyboard


def get_msg_urls(message):
    urls = []
    for x in message.entities:
        if x.type in ["url", "text_link"]:
            p1 = x.offset
            p2 = p1 + x.length
            urls.append(message.text[p1:p2])
    return urls
