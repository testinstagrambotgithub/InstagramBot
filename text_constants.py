ADMIN_ID = 1308747692
GROUP_ID = 1001152231184
TOKEN = "1589253689:AAFCxt2kV0h4mFrrrCn4Y1pjLnxuk4dFq9M"
DX_QUANTITY = 5


def welcome_message(first_name):
    welcome_message_text = """ Hello, {}. ☺
Welcome to our Engagement Group! Please read the rules carefully.
    """.format(first_name)
    return welcome_message_text


def admin_start_message(first_name):
    admin_start_message_text = """ <b>{}</b>, Welcome to Admin Panel 😎
    Take a look at our available features!
    """.format(first_name)
    return admin_start_message_text


def user_start_message(username):
    user_start_message_text = """ Hello @<b>{}</b>! 😊
Glad you want to join our Engagement Group.

Please carefully read the rules and make sure that your Instagram username is the same as your Telegram username. 

Otherwise, we can't guarantee 100% functionality. 
    """.format(username)
    return user_start_message_text


warning_message = "You posted the wrong format! READ RULES! ⛔"

packages_message = """
"Which product do you want to buy? 

<b>⭐ Golden Package - € 59.99</b>
You want to boost your Instagram and start off with your first Engagement Group experiences?
Get your Golden Package now and get the following benefits:
- Access to our exclusive Telegram Engagement Group
- Access to an exclusive Instagram Engagement Group fitting your niche

<b>💎 Diamond Package - € 89.99</b>
The Instagram Diamond Package contains everything you need to start an awesome account!
You will receive the following benefits:
- Access to an Instagram Engagement Group or your Niche
- Access to our Telegram Group
- Instagram Growth e-book
- Instagram Growth Presentation
- Hashtag compilation with more than 500! Hashtags
- 20% off our preset bundles ”
"""
