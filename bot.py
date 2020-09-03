from telebot import TeleBot
from config import Config
from lang import Translate
from db import DB
import bot_utils

config = Config()
bot = TeleBot(token=config.token)
tl = Translate(lang=config.lang, cfg_dict=config.dict)

@bot.message_handler(commands=["register"])
def register_reviewer(message):
    reviewer = message.from_user.username
    if not reviewer:
        bot.send_message(message.chat.id,
                         text=tl.get("The telegram username (user id) should be set. Please have it set in profile"))
        return None
    db = DB()

    if db.is_reviewer_exists(chat_id=message.chat.id, reviewer=reviewer):
        s = tl.get("already registered")
    else:
        db.add_reviewer(chat_id=message.chat.id, reviewer=reviewer)
        s = tl.get("successfully registered!")
    db.close()

    bot.send_message(message.chat.id, text=f"@{reviewer} {s}")


@bot.message_handler(commands=["unregister"])
def unregister_reviewer(message):
    reviewer = message.from_user.username
    db = DB()
    if db.is_reviewer_exists(chat_id=message.chat.id, reviewer=reviewer):
        db.delete_reviewer(chat_id=message.chat.id, reviewer=reviewer)
        s = tl.get("successfully left the bot")
    else:
        s = tl.get("already left the bot")
    db.close()
    bot.send_message(message.chat.id, text=f"@{reviewer} {s}")


@bot.message_handler(commands=["reviewers"])
def show_reviewers(message):
    db = DB()
    items = map(lambda x: f"{x[0]}, {x[1]}", db.get_reviewers(chat_id=message.chat.id))
    text = "\n".join(items) or "🤷"
    db.close()
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=["next"])
def show_next(message):
    db = DB()
    text = db.who_next_reviewer(chat_id=message.chat.id) or "🤷"
    db.close()
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=["review"])
def review(message):
    urls = bot_utils.get_msg_urls(message)
    if not urls:
        bot.send_message(message.chat.id,
                         text=tl.get("The link is required to review. Add your link after the command /review"))
        return None

    reporter = message.from_user.username
    reviewers = bot_utils.get_msg_usernames(message)

    if not reviewers:
        db = DB()
        reviewer = db.get_next_reviewer(chat_id=message.chat.id, reporter=reporter)
        if reviewer:
            reviewers.append(f"@{reviewer}")
        db.close()

    if not reviewers:
        bot.send_message(message.chat.id,
                         text=tl.get(
                             "There are no registered reviewers in the bot. Ask them to register with the command /register"))
        return None

    s = tl.get("Who wants to review?")
    reviewers_as_text = " ".join(reviewers)
    keyboard = bot_utils.create_callback_button({tl.get("Take!"): reporter})
    bot.send_message(message.chat.id, text=f"{s}\n{urls[0]}\n{reviewers_as_text}", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        chat_id = call.message.chat.id
        reporter = call.data
        reviewer_first_name = call.from_user.first_name
        reviewer = call.from_user.username

        if reporter == reviewer:
            bot.send_message(chat_id=chat_id, text=tl.get("It is not allowed to review yourself!"))
            return None

        db = DB()
        if not db.is_reviewer_exists(chat_id=chat_id, reviewer=reviewer):
            s = tl.get("please register first with the command /register")
            bot.send_message(chat_id=chat_id,
                             text=f"@{reviewer}, {s}")
            db.close()
            return None
        db.update_time(chat_id=chat_id, reviewer=reviewer)
        db.close()

        s = tl.get("your review has been taken by")
        bot.reply_to(call.message, f"@{reporter}, {s} {reviewer_first_name}")
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text=call.message.text, reply_markup=None)


if __name__ == '__main__':
    bot.polling(none_stop=True)
