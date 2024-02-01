# SSH Telegram Bot

This bot helps you to manage and interact with your VPS through SSH protocol using telegram.


## Setup Guide
 Open `bot.py` and replace your bot information.
> - Replace  `TOKEN` value with the **token** you receive after creating your telegram bot using [@botfather](https://t.me/botfather)
> - Replace `BOT_USERNAME` value with the **username** of your telegram bot.
>
>example:
>![Image](https://i.postimg.cc/pdM0Ls8Q/Screenshot-2024-01-24-at-4-13-12-PM.png)

Open `admins.txt` and replace the initial number with your **Telegram user ID**
> To get your Telegram user ID you can use [@userinfobot](https://t.me/userinfobot)

You should be good to go :)

## Commands and Usage

After starting the bot, you have to **add your server**. use :
`/add_server [SERVER_IP] [LOGIN_USERNAME] [LOGIN_PASSWORD]`
> For example:
> `/add_server 198.168.1.1 root admin`
> - You can add multiple servers using this command
> -  if you enter a valid IP and login information you should see your server added successfully to the robot. *(and servers.txt)*

You can see the **list of servers you added** with:
`/my_servers`

Now you can **connect to a server using**:
`/connect [SERVER_ID]`
> - Use the SERVER_ID that you received after adding a server to your server list.
> - If you missed your SERVER_ID, can find it again using `/my_servers` command.

after connecting to your server you can run different commands and see the output of them through your telegram bot.
> Example: 
> ![enter image description here](https://i.postimg.cc/85Td95fM/Screenshot-2024-01-24-at-4-39-06-PM.png)

If you want to **disconnect** from your server use `/disconnect` command.

## Todo

-  [ ] Add option to download files...
-  [ ] add option to upload files...
-  [ ] Add Interactive commands...
- [ ] Optimizing the output shown by the bot...

*Also contributions of all sizes are very welcome. :)))*
