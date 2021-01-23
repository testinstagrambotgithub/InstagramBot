import telebot
from telebot import types
import helper
import text_constants

from instagram_handler import InstagramHandler
from database_handler import DatabaseHandler

bot = telebot.TeleBot(text_constants.TOKEN)

instagram_handler = InstagramHandler()
instagram_handler.setup_session()

database_handler = DatabaseHandler()
database_handler.create_table_members()
database_handler.create_table_links()
database_handler.create_table_codes()


@bot.message_handler(content_types=["new_chat_members"])
def handle_new_joined_users(message):
    database_handler.update_table_members(message.from_user.first_name,
                                          message.from_user.last_name,
                                          message.from_user.id)
    bot.reply_to(message, text_constants.welcome_message(message.from_user.first_name))


def send_welcome_admin(message):
    bot.send_message(message.from_user.id,
                     text_constants.admin_start_message(message.from_user.username),
                     parse_mode="HTML")


def send_welcome_not_admin(message):
    id = message.from_user.id
    bot.send_message(id, text_constants.user_start_message(message.from_user.username), parse_mode="HTML")

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="Yes", callback_data="gdpr_button_accepted"))
    file = open("GDPR.pdf", "rb")
    bot.send_document(id, file)
    bot.send_message(id, "Do you accept our GDPR(General Data Protection Regulation)?", reply_markup=keyboard)


@bot.message_handler(commands=['start'], func=lambda message: message.chat.id == message.from_user.id)
def send_welcome(message):
    if message.from_user.id == text_constants.ADMIN_ID:
        send_welcome_admin(message)
    else:
        send_welcome_not_admin(message)


@bot.message_handler(commands=['list'], func=lambda message: message.chat.id == message.from_user.id)
def send_list(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="10", callback_data="like_10_pictures"))
    keyboard.add(types.InlineKeyboardButton(text="20", callback_data="like_20_pictures"))
    keyboard.add(types.InlineKeyboardButton(text="35", callback_data="like_35_pictures"))
    keyboard.add(types.InlineKeyboardButton(text="50", callback_data="like_50_pictures"))
    bot.send_message(message.chat.id, "How many pictures do you want to like?", reply_markup=keyboard)


@bot.message_handler(commands=['create_code'], func=lambda message: message.chat.id == message.from_user.id)
def create_code(message):
    codes = database_handler.get_all_codes()
    msg = bot.send_message(message.chat.id, "Enter your new code and discount in this format: <b>CODE DISCOUNT</b>. "
                                      "For example: MyNewCode 20", parse_mode="HTML")
    for code in codes:
        bot.send_message(message.chat.id, "Code - " + str(code[0]) + " and discount - " + str(code[1]) + "%")
    bot.register_next_step_handler(msg, create_new_code)


@bot.message_handler(commands=['get_all_codes'], func=lambda message: message.chat.id == message.from_user.id)
def get_all_codes(message):
    codes = database_handler.get_all_codes()
    for code in codes:
        print(code)
        bot.send_message(message.chat.id, str(code))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        id = call.message.chat.id
        if call.data == "gdpr_button_accepted":
            bot.edit_message_text(chat_id=id, message_id=call.message.message_id, text="Thank you! 😊")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="⭐ Golden Package", callback_data="golden_package"))
            keyboard.add(types.InlineKeyboardButton(text="💎 Diamond Package", callback_data="diamond_package"))
            bot.send_message(id, text=text_constants.packages_message, parse_mode="HTML", reply_markup=keyboard)

        elif call.data == "golden_package":
            bot.edit_message_text(chat_id=id, message_id=call.message.message_id, text=text_constants.packages_message, parse_mode="HTML")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Pay", callback_data="pay_golden"))
            keyboard.add(types.InlineKeyboardButton(text="Code", callback_data="code_golden"))
            bot.send_message(id, text="Do you want to pay or do you have a code?", parse_mode="HTML", reply_markup=keyboard)
        elif call.data == "diamond_package":
            bot.edit_message_text(chat_id=id, message_id=call.message.message_id, text=text_constants.packages_message, parse_mode="HTML")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Pay", callback_data="pay_diamond"))
            keyboard.add(types.InlineKeyboardButton(text="Code", callback_data="code_diamond"))
            bot.send_message(id, text="Do you want to pay or do you have a code?", parse_mode="HTML",  reply_markup=keyboard)

        elif call.data == "pay_golden":
            bot.send_message(id, text="Please contact us to pay via Stripe")
        elif call.data == "code_golden":
            message = bot.send_message(id, text="Please enter your code")
            bot.register_next_step_handler(message, ask_for_code)
        elif call.data == "pay_diamond":
            bot.send_message(id, text="Please contact us to pay via Stripe")
        elif call.data == "code_diamond":
            message = bot.send_message(id, text="Please enter your code")
            bot.register_next_step_handler(message, ask_for_code)

        elif call.data == "like_10_pictures":
            links = database_handler.get_latest_photos(10)
            bot.edit_message_text(chat_id=id, message_id=call.message.message_id,
                                  text="There you go 😊\nPlease 👍 every link below",
                                  parse_mode="HTML")
            for link in links:
                correct_link = "https://www.instagram.com/p/" + str(link[0]) + "/"
                bot.send_message(id, text=str(correct_link), disable_web_page_preview=True)

            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Done", callback_data="done"))
            bot.send_message(id, text="If you liked every picture please submit with the done button below", reply_markup=keyboard)

        elif call.data == "like_20_pictures":
            links = database_handler.get_latest_photos(20)
            bot.edit_message_text(chat_id=id, message_id=call.message.message_id,
                                  text="There you go 😊\nPlease 👍 every link below",
                                  parse_mode="HTML")
            for link in links:
                correct_link = "https://www.instagram.com/p/" + str(link[0]) + "/"
                bot.send_message(id, text=str(correct_link), disable_web_page_preview=True)

            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Done", callback_data="done"))
            bot.send_message(id, text="If you liked every picture please submit with the done button below",
                             reply_markup=keyboard)

        elif call.data == "like_35_pictures":
            links = database_handler.get_latest_photos(35)
            bot.edit_message_text(chat_id=id, message_id=call.message.message_id,
                                  text="There you go 😊\nPlease 👍 every link below",
                                  parse_mode="HTML")
            for link in links:
                correct_link = "https://www.instagram.com/p/" + str(link[0]) + "/"
                bot.send_message(id, text=str(correct_link), disable_web_page_preview=True)

            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Done", callback_data="done"))
            bot.send_message(id, text="If you liked every picture please submit with the done button below",
                             reply_markup=keyboard)

        elif call.data == "like_50_pictures":
            links = database_handler.get_latest_photos(50)
            bot.edit_message_text(chat_id=id, message_id=call.message.message_id,
                                  text="There you go 😊\nPlease 👍 every link below",
                                  parse_mode="HTML")
            for link in links:
                correct_link = "https://www.instagram.com/p/" + str(link[0]) + "/"
                bot.send_message(id, text=str(correct_link), disable_web_page_preview=True)

            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Done", callback_data="done"))
            bot.send_message(id, text="If you liked every picture please submit with the done button below",
                             reply_markup=keyboard)

        elif call.data == "done":
            bot.edit_message_text(chat_id=id, message_id=call.message.message_id,
                                  text="Thank you! Give me some time to check. I will let you know when I am ready")
            liked = instagram_handler.check_that_user_liked_all_photos(call.message.chat.username)
            if liked:
                msg = bot.send_message(id, text="Great job! 🙌\nYou liked every picture, now it's our turn. Please enter the link to your Instagram post.")
                bot.register_next_step_handler(msg, ask_user_for_link)
            else:
                bot.send_message(id, text="You have missed some pictures")


def ask_user_for_link(message):
    text = message.text
    if len(text.split()) == 1:
        photo_id = text.split('/p/')[1].split('/')[0]
        database_handler.update_table_links(photo_id, "None", 0)
        bot.reply_to(message, "Thank you")


def ask_for_code(message):
    try:
        codes = database_handler.get_all_codes()
        for code in codes:
            if str(message.text) == str(code[0]):
                bot.reply_to(message, "This code gives you " + str(code[1]) + "% discount! Please contact us")
    except Exception as e:
        print(e)


def create_new_code(message):
    try:
        code = str(message.text).split()[0]
        discount = str(message.text).split()[1]

        if int(discount) > 100 or int(discount) < 0:
            bot.reply_to(message, "Discount must be in the range [0, 100]")
        else:
            database_handler.update_table_codes(code, discount)
            bot.reply_to(message, "The code has been added")
    except Exception as e:
        print(e)


bot.polling()
