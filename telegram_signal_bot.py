import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from bot import analyze
from config import TELEGRAM_BOT_TOKEN

# ==========================================
# FORMATEAR MENSAJE
# ==========================================

def format_signal(best):

    return f"""
🚀 CRYPTO AI SIGNAL

🪙 {best['symbol']}

💰 Precio:
{best['price']}

🛑 Stop Loss:
{best['stop_loss']}

🎯 Take Profit:
{best['take_profit']}

📦 Tamaño posición:
{best['position_size']}

📈 Probabilidad:
{best['probability']}%

🧠 Score:
{best['score']}

📰 Sentimiento:
{best['sentiment']}
"""

# ==========================================
# HANDLER PRINCIPAL
# ==========================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    if "obtener señal" in text:

        await update.message.reply_text("🔎 Analizando mercado...")

        try:

            results = analyze()

            if not results:

                await update.message.reply_text("❌ No se encontraron resultados")
                return

            best = results[0]

            message = format_signal(best)

            await update.message.reply_text(message)

        except Exception as e:

            await update.message.reply_text(f"❌ Error: {str(e)}")

    else:

        await update.message.reply_text(
            "Escribe: Obtener Señal"
        )

# ==========================================
# MAIN
# ==========================================

def main():

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot corriendo...")

    app.run_polling()

# ==========================================

if __name__ == "__main__":
    main()