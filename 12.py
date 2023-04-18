from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# create an inline keyboard with a single button
inline_keyboard = [[InlineKeyboardButton("My Inline Button", callback_data="my_callback_data")]]
inline_markup = InlineKeyboardMarkup(inline_keyboard)

# create a reply keyboard with a single button
reply_keyboard = [[KeyboardButton("My Reply Button")]]
reply_markup = ReplyKeyboardMarkup(reply_keyboard)

# merge the inline and reply keyboard buttons into a single keyboard
keyboard = inline_markup.inline_keyboard + reply_markup.keyboard

# create a reply keyboard markup with both buttons
markup = ReplyKeyboardMarkup(keyboard)

# send the message with both keyboards
context.bot.send_message(chat_id=update.effective_chat.id, text="Here are both keyboards together!", reply_markup=markup)
