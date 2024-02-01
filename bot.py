from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputTextMessageContent
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, ConversationHandler
from time import gmtime, strftime
from commands import do_command
from authentication import isAdminUser, add_admin_to_file
from servers import get_servers_data, is_valid_ip, del_server, is_valid_login, add_server, client


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to **SSH Terminal Bot**\nInteract easily with your server through me :)', parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please check the repository for command guides :)')

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if isAdminUser(update.message.chat.id):
        data: str = update.message.text
        proccessed_data: str = data.replace("/add_admin", '').strip()
        print(f">> new admin added by ({update.message.chat.username} {update.message.chat.id}). \n{proccessed_data} is now admin,\n")
        add_admin_to_file(proccessed_data)
        await update.message.reply_text(f"New admin added \n{proccessed_data} is now admin.")
    else:
        await update.message.reply_text("You dont have access to add a new admin.")


async def del_server_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender: str = update.message.chat.id
    if isAdminUser(update.message.chat.id) or isAdminUser(update.message.chat.username):
            data: str = update.message.text
            proccessed_data: int = int(str(data.replace("/del_server", '').strip()))
            servers = get_servers_data()
            if int(proccessed_data) <= len(servers):
                del_server(int(proccessed_data))
                print(int(proccessed_data), len(servers))
                print(f'>> A server deleted by ({update.message.chat.username} {update.message.chat.id})\n - Server IP : {servers[proccessed_data-1][0]}\n - Connection Info : {servers[proccessed_data-1][1]}:{servers[proccessed_data-1][2]}',
                    end="")
                await update.message.reply_text(f'Server Deleted\n'
                                                    f'Server IP : {servers[proccessed_data - 1][0]}\n'
                                                    f'Connection Info : {servers[proccessed_data - 1][1]}:{servers[proccessed_data - 1][2]}\n'
                                                    f'Deleted by : {sender} in {strftime("%Y-%m-%d %H:%M:%S", gmtime())}\n')
            else:
                await update.message.reply_text(f'Server doesnt exist, try again')
    else:
        await update.message.reply_text(f'You need admin access to delete to a server!')
async def add_server_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender: str = update.message.chat.id
    if isAdminUser(update.message.chat.id) or isAdminUser(update.message.chat.username):
        data: str = update.message.text
        proccessed_data: str = data.replace("/add_server", '').strip()
        proccessed_data_list = proccessed_data.split()
        await update.message.reply_text(f'Checking validity of given ip')
        if is_valid_ip(proccessed_data_list[0]):
            await update.message.reply_text(f'IP validation successful.')
            await update.message.reply_text(f'Checking validity of login information')
            if is_valid_login(proccessed_data_list[0] , proccessed_data_list[1] , proccessed_data_list[2]):
                await update.message.reply_text(f'Login information validation successful.')
                add_server(proccessed_data_list[0] , proccessed_data_list[1] , proccessed_data_list[2] , sender , strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                print(f">> Adding a new server by : ({update.message.chat.username} {update.message.chat.id}).\n"
                      f"    servers_list- Server Info: {proccessed_data}")
                await update.message.reply_text(f'New server added! (status : Unknown)\n'
                                                f'Server IP : {proccessed_data_list[0]}\n'
                                                f'Connection Info : {proccessed_data_list[1]}:{proccessed_data_list[2]}\n'
                                                f'added by : {sender} in {strftime("%Y-%m-%d %H:%M:%S", gmtime())}\n')
            else:
                await update.message.reply_text(f'Adding new server failed!\nEither username or password is not correct\nPlease try again.')
        else:
            await update.message.reply_text(f'Adding new server failed!\nPlease enter a valid IP.')
    else:
        await update.message.reply_text(f'You need admin access to add a new server!')
async def servers_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender: str = update.message.chat.id
    if isAdminUser(update.message.chat.id) or isAdminUser(update.message.chat.username):
        print(f">> List of servers asked by : ({update.message.chat.username} {update.message.chat.id}).")
        servers = get_servers_data()
        table = "All Servers:\n\n\n"
        counter = 1
        for server in servers:
            table += (f"Server Number : {counter}\n"
                      f"Server IP : {server[0]}\n"
                      f"Added By : {server[3]}\n"
                      f"Date Added : {server[4]}\n\n---------\n")
            counter += 1
        await update.message.reply_text(table)
    else:
        await update.message.reply_text(f'You need admin access to view list of servers!')

async def connect_to_server_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender: str = update.message.chat.id
    global is_connected_to_server
    if isAdminUser(update.message.chat.id) or isAdminUser(update.message.chat.username):
        if is_connected_to_server is False:
            data: str = update.message.text
            proccessed_data: str = data.replace("/connect", '').strip()
            proccessed_data = int(proccessed_data) - 1
            servers = get_servers_data()
            print(f'>> Trying to connect to server by ({update.message.chat.username} {update.message.chat.id})\n - Server IP : {servers[proccessed_data][0]}\n - Connection Info : {servers[proccessed_data][1]}:{servers[proccessed_data][2]}\n - Result : ',
                end="")
            await update.message.reply_text(f'Trying to connect to server\n'
                                                f'Server IP : {servers[proccessed_data][0]}\n'
                                                f'Connection Info : {servers[proccessed_data][1]}:{servers[proccessed_data][2]}\n'
                                                f'added by : {servers[proccessed_data][3]} in {servers[proccessed_data][4]}\n')
            try:
                client.connect(servers[proccessed_data][0], username=servers[proccessed_data][1],
                                password=servers[proccessed_data][2])
                print("Successfull!!\n")
                is_connected_to_server = True
                await update.message.reply_text(f'Successfully connected to server!')
            except:
                print("Failed!\n")
                is_connected_to_server = False
                await update.message.reply_text(f'Couldn\'t connected to server!')
        else:
            await update.message.reply_text(f'Already connected to server\nplease disconnect first using:\n/disconnect command')
    else:
        await update.message.reply_text(f'You need admin access to connect to a server!')


async def discconnect_from_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_connected_to_server
    if isAdminUser(update.message.chat.id) or isAdminUser(update.message.chat.username):
        print(
            f'>> Trying to close the connection by ({update.message.chat.username} {update.message.chat.id})\n - Result : ',
            end="")
        if is_connected_to_server is True:
            client.close()
            is_connected_to_server = False
            print("Successfully closed the connection\n")
            await update.message.reply_text("Connection closed!")
        else:
            print("Failed - no connection found!\n")
            await update.message.reply_text("Failed to do the task! (you sure I was connected to a server?)")
    else:
        await update.message.reply_text(f'You need admin access to disconnect from a server!')

def handle_command(text: str) -> str:
    proccessed_text = text.lower()
    global is_connected_to_server
    if is_connected_to_server is True:
        result = do_command(client, proccessed_text)
        return f"*Done!*\n```shell\n{proccessed_text}\n```\n*output:*\n```\n{result}```"
    else:
        return f"Im not connected to any server.\nPlease connect me with /connect command"

async def command_handler(update: Update, context:ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'>> user ({update.message.chat.first_name} {update.message.chat.last_name}) in {message_type}: "{text}"')

    if message_type == 'group' or message_type == 'supergroup':
        await update.message.reply_text(f'Currently Im not able to execute commands given in groups!\nPls dm me!')
        return
    else:
        response: str = handle_command(text)

    await update.message.reply_text(response, parse_mode="markdown")


async def error(update: Update, context:ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused {context.error}')

