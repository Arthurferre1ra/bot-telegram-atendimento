from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

class LojaBot:
    def __init__(self):
        # Inicializa os dados básicos do bot
        self.smartphones = ["iPhone 14", "Samsung Galaxy S23", "Xiaomi Mi 13"]
        self.feedback_email = "feedback@loja.com"
        self.user_orders = {}  # Dicionário para salvar os pedidos dos usuários

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Inicializa o bot para o usuário, criando seu registro e mostrando o menu inicial.
        """
        user = update.effective_user
        if user.id not in self.user_orders:
            # Cria uma entrada para o usuário, se não existir
            self.user_orders[user.id] = {"Smartphones": [], "Capas e Películas": []}
        await self.show_menu(update)  # Exibe o menu principal

    async def show_menu(self, update: Update) -> None:
        """
        Mostra o menu principal de opções ao usuário.
        """
        keyboard = [
            ["📱 Smartphones", "📦 Capas & Películas"],
            ["🛡️ Garantia", "✉️ Feedback"],
            ["📋 Resumo do Pedido"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Escolha uma opção abaixo:", reply_markup=reply_markup)

    async def handle_smartphones(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Lista os modelos de smartphones disponíveis e solicita ao usuário que selecione um.
        """
        message = "📱 *Modelos disponíveis para venda:*\n"
        for idx, modelo in enumerate(self.smartphones, 1):
            message += f"{idx}. {modelo}\n"
        message += "\nPor favor, responda com o número do modelo desejado."
        await update.message.reply_text(message, parse_mode="Markdown")
        context.user_data["awaiting_selection"] = "smartphone"  # Define o tipo de seleção aguardada

    async def handle_capas_peliculas(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Lista os modelos disponíveis para capas e películas e solicita a seleção do usuário.
        """
        message = "📦 *Modelos disponíveis para capas e películas:*\n"
        for idx, modelo in enumerate(self.smartphones, 1):
            message += f"{idx}. {modelo}\n"
        message += "\nPor favor, responda com o número do modelo desejado."
        await update.message.reply_text(message, parse_mode="Markdown")
        context.user_data["awaiting_selection"] = "capa"  # Define o tipo de seleção aguardada

    async def process_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Processa a seleção feita pelo usuário com base no tipo de item (smartphone ou capa).
        """
        user_id = update.effective_user.id
        selection_type = context.user_data.get("awaiting_selection")  # Obtém o tipo de seleção aguardada

        if not selection_type:
            # Caso não haja seleção aguardada, exibe uma mensagem de erro
            await update.message.reply_text("Desculpe, não entendi. Escolha uma opção do menu.")
            return

        try:
            choice = int(update.message.text) - 1  # Converte a entrada para índice
            if 0 <= choice < len(self.smartphones):
                selected_item = self.smartphones[choice]
                if selection_type == "smartphone":
                    # Adiciona o smartphone ao pedido do usuário
                    self.user_orders[user_id]["Smartphones"].append(selected_item)
                    await update.message.reply_text(f"✅ Você adicionou *{selected_item}* ao seu pedido.", parse_mode="Markdown")
                elif selection_type == "capa":
                    # Adiciona a capa e película ao pedido do usuário
                    self.user_orders[user_id]["Capas e Películas"].append(selected_item)
                    await update.message.reply_text(f"✅ Você adicionou capas e películas para *{selected_item}* ao seu pedido.", parse_mode="Markdown")
            else:
                raise ValueError  # Dispara erro caso o número esteja fora do intervalo
        except ValueError:
            await update.message.reply_text("❌ Por favor, informe um número válido.")
        finally:
            context.user_data["awaiting_selection"] = None  # Limpa o marcador de seleção
            await self.show_menu(update)  # Retorna ao menu principal

    async def handle_garantia(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Solicita as informações necessárias para o atendimento de garantia.
        """
        await update.message.reply_text(
            "🛡️ *Garantia:*\nPor favor, informe seu *nome* e o *motivo do retorno* no formato:\n\n"
            "`Nome: Seu Nome\nMotivo: Descreva o problema`",
            parse_mode="Markdown"
        )
        await self.show_menu(update)

    async def handle_feedback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Exibe o e-mail para envio de feedback.
        """
        await update.message.reply_text(
            f"✉️ *Feedback:*\nPor favor, envie seu feedback para o e-mail abaixo:\n\n`{self.feedback_email}`",
            parse_mode="Markdown"
        )
        await self.show_menu(update)

    async def resumo_pedido(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Exibe o resumo do pedido do usuário, mostrando os itens selecionados.
        """
        user_id = update.effective_user.id
        pedidos = self.user_orders.get(user_id, {})
        if not pedidos or all(not items for items in pedidos.values()):
            await update.message.reply_text("📋 Você ainda não adicionou nada ao seu pedido.")
        else:
            resumo = "📋 *Resumo do seu pedido:*\n"
            for categoria, itens in pedidos.items():
                if itens:
                    resumo += f"\n*{categoria}:*\n" + "\n".join(f"- {item}" for item in itens)
            await update.message.reply_text(resumo, parse_mode="Markdown")
        await self.show_menu(update)

    async def handle_unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Lida com mensagens desconhecidas, exibindo uma mensagem de erro e o menu novamente.
        """
        await update.message.reply_text(
            "Desculpe, não entendi sua mensagem. Escolha uma opção do menu abaixo:",
            reply_markup=ReplyKeyboardMarkup(
                [["📱 Smartphones", "📦 Capas & Películas"], ["🛡️ Garantia", "✉️ Feedback"], ["📋 Resumo do Pedido"]],
                resize_keyboard=True
            )
        )

# Configurar e iniciar o bot
def main():
    """
    Configura e inicia o bot com os handlers apropriados.
    """
    # Substitua 'YOUR_BOT_TOKEN' pelo token do seu bot fornecido pelo BotFather
    token = "Seu token"
    loja_bot = LojaBot()

    application = Application.builder().token(token).build()

    # Configurar handlers
    application.add_handler(CommandHandler("start", loja_bot.start))
    application.add_handler(MessageHandler(filters.Regex("📱 Smartphones"), loja_bot.handle_smartphones))
    application.add_handler(MessageHandler(filters.Regex("📦 Capas & Películas"), loja_bot.handle_capas_peliculas))
    application.add_handler(MessageHandler(filters.Regex("📋 Resumo do Pedido"), loja_bot.resumo_pedido))
    application.add_handler(MessageHandler(filters.Regex("🛡️ Garantia"), loja_bot.handle_garantia))
    application.add_handler(MessageHandler(filters.Regex("✉️ Feedback"), loja_bot.handle_feedback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, loja_bot.process_selection))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, loja_bot.handle_unknown))

    # Executar o bot
    application.run_polling()

if __name__ == "__main__":
    main()
