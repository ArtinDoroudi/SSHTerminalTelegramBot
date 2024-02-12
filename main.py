from typing import Final
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, ConversationHandler
from bot import start_command, help_command, add_admin, add_server_handler, del_server_handler, servers_list, connect_to_server_handler, discconnect_from_server, command_handler


TOKEN: Final= '6985915535:AAGu5GIxT6QkNymDXIc2yT9VnObsM4e5jq4'
BOT_USERNAME : Final = "@MyBot"

if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('add_admin', add_admin))
    app.add_handler(CommandHandler('add_server', add_server_handler))
    app.add_handler(CommandHandler('del_server', del_server_handler))
    app.add_handler(CommandHandler('servers_list', servers_list))
    app.add_handler(CommandHandler('connect', connect_to_server_handler))
    app.add_handler(CommandHandler('disconnect', discconnect_from_server))
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, command_handler))

    # Errors
    #app.error_handlers(error)

    print("Starting...")
    app.run_polling(poll_interval=3)