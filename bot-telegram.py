from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Definir modelos disponíveis
smartphones = ["iPhone 14", "Samsung Galaxy S23", "Xiaomi Mi 13"]
capas_peliculas = ["iPhone", "Samsung", "Xiaomi"]
feedback_email = "feedback@loja.com"

# Função para iniciar o bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_message = f"Olá, {user.first_name}! Bem-vindo ao atendimento da nossa loja.\n\nEscolha uma opção abaixo:"
    keyboard = [
        ["📱 Smartphones", "📦 Capas & Películas"],
        ["🛡️ Garantia", "✉️ Feedback"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Função para listar smartphones
async def handle_smartphones(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📱 *Modelos disponíveis para venda:*\n" +
        "\n".join(f"- {modelo}" for modelo in smartphones),
        parse_mode="Markdown"
    )

# Função para listar marcas de capas e películas
async def handle_capas_peliculas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📦 *Marcas disponíveis com capas e películas:*\n" +
        "\n".join(f"- {marca}" for marca in capas_peliculas),
        parse_mode="Markdown"
    )

# Função para lidar com garantia
async def handle_garantia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🛡️ *Garantia:*\nPor favor, informe seu *nome* e o *motivo do retorno* no formato:\n\n"
        "`Nome: Seu Nome\nMotivo: Descreva o problema`",
        parse_mode="Markdown"
    )

# Função para lidar com feedback
async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"✉️ *Feedback:*\nPor favor, envie seu feedback para o e-mail abaixo:\n\n`{feedback_email}`",
        parse_mode="Markdown"
    )

# Função para tratar mensagens não reconhecidas
async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Desculpe, não entendi sua mensagem. Escolha uma opção do menu abaixo:",
        reply_markup=ReplyKeyboardMarkup(
            [["📱 Smartphones", "📦 Capas & Películas"], ["🛡️ Garantia", "✉️ Feedback"]],
            resize_keyboard=True
        )
    )

# Função principal
def main():
    # Substitua 'YOUR_BOT_TOKEN' pelo token do seu bot fornecido pelo BotFather
    token = "Seu token"

    # Criar aplicação
    application = Application.builder().token(token).build()

    # Configurar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("📱 Smartphones"), handle_smartphones))
    application.add_handler(MessageHandler(filters.Regex("📦 Capas & Películas"), handle_capas_peliculas))
    application.add_handler(MessageHandler(filters.Regex("🛡️ Garantia"), handle_garantia))
    application.add_handler(MessageHandler(filters.Regex("✉️ Feedback"), handle_feedback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unknown))

    # Executar o bot
    application.run_polling()

if __name__ == "__main__":
    main()
