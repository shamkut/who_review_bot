from telebot import TeleBot
from config import Config
from db import DB
import bot_utils
from datetime import datetime

config = Config()
bot = TeleBot(config.token, parse_mode=None)


@bot.message_handler(commands=["register"])
def register_reviewer(message):
    reviewer = message.from_user.username
    db = DB()
    if not db.is_reviewer_exists(chat_id=message.chat.id, reviewer=reviewer):
        db.add_reviewer(chat_id=message.chat.id, reviewer=reviewer)
        text = f"@{reviewer} успешно зарегистрирован!"
    else:
        text = f"@{reviewer} уже есть"
    db.close()
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=["unregister"])
def unregister_reviewer(message):
    reviewer = message.from_user.username
    db = DB()
    if db.is_reviewer_exists(chat_id=message.chat.id, reviewer=reviewer):
        db.delete_reviewer(chat_id=message.chat.id, reviewer=reviewer)
        text = f"@{reviewer} успешно покинул бота"
    else:
        text = f"@{reviewer} уже покинул бота"
    db.close()
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=["reviewers"])
def show_reviewers(message):
    db = DB()
    text = "\n".join(db.get_reviewers(chat_id=message.chat.id)) or "🤷"
    db.close()
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=["next"])
def show_next(message):
    db = DB()
    text = db.who_next_reviewer(chat_id=message.chat.id)
    db.close()
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=["review"])
def review(message):
    urls = bot_utils.get_msg_urls(message)
    if not urls:
        bot.send_message(message.chat.id,
                         text="Для ревью нужна ссылка. Добавьте ссылку после команды /review")
        q[message.chat.id] = [message.from_user.username, datetime.now()]
        return None

    reporter = message.from_user.username

    db = DB()
    reviewer = db.get_next_reviewer(chat_id=message.chat.id, reporter=reporter)
    db.close()

    if not reviewer:
        bot.send_message(message.chat.id,
                         text="Нет зарегистрированных ревьюверов. Попросите их зарегистрироваться командой /register")
        return None

    text = f"{config.review_question}\n{urls[0]}\n@{reviewer}"
    keyboard = bot_utils.create_callback_button({config.button_title: reporter})
    bot.send_message(message.chat.id, text=text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        reporter = call.data
        reviewer_first_name = call.from_user.first_name
        reviewer = call.from_user.username

        db = DB()
        db.update_time(chat_id=call.message.chat.id, reviewer=reviewer)
        db.close()

        bot.reply_to(call.message, f"@{reporter}, {reviewer_first_name} взял на ревью!")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=call.message.text, reply_markup=None)


if __name__ == '__main__':
    bot.polling(none_stop=True)
