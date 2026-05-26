from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from bot import analyze

from config import TELEGRAM_BOT_TOKEN

DASHBOARD_URL = "cryptoaibot..streamlit.app"

# ==========================================
# START
# ==========================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🚀 Escribe:\n\nObtener Señal"
    )

# ==========================================
# MESSAGE
# ==========================================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text.lower()

    if text == "obtener señal":

        await update.message.reply_text(
            "📊 Analizando mercado..."
        )

        results = analyze()

        best = results[0]

        ranking = ""

        for i, coin in enumerate(
            results,
            start=1
        ):

            ranking += (
                f"{i}. "
                f"{coin['symbol']} | "
                f"{coin['probability']}%\n"
            )

        message = f"""
🚀 CRYPTO AI DASHBOARD

🏆 MEJOR SEÑAL

🪙 {best['symbol']}

💰 Precio:
{best['price']}

🛑 Stop Loss:
{best['stop_loss']}

🎯 Take Profit:
{best['take_profit']}

📈 Probabilidad:
{best['probability']}%

📰 Sentimiento:
{best['sentiment']}

⭐ Score:
{best['score']}

📊 TOP CRYPTOS

{ranking}
"""

        await update.message.reply_text(
            message
        )

# ==========================================
# RUN BOT
# ==========================================

app = ApplicationBuilder().token(
    TELEGRAM_BOT_TOKEN
).build()

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT,
        message_handler
    )
)

print("BOT INICIADO")

app.run_polling()