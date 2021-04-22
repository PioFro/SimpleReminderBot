# Reminder Bot for Discord
### How to add already running bot?
Use this link https://discord.com/api/oauth2/authorize?client_id=831147000032395284&permissions=76800&scope=bot to add this bot to your channel.
### How to run it myself?
Follow this guide https://realpython.com/how-to-make-a-discord-bot-python/ and create a file called token with the token.
## Commands
### !add
#### Required parameters
* date+hour - format dd.mm.yy-HH:MM, example 10.02.21-13:32 
#### Optional parameters
* -r - Is the reminder recurring? By default False.
* -i - Interval between reminders. Possible intervals (d)ay, (h)our, (m)inute. Example 1d.
* -m - Message that will be sent each time the trigger occurs. Example: "This is a sample message. 1 2 3"
#### Example command
```bash
!add date+hour 10.01.21-10:21 -m Sample msg -r -i 1m
```
Example command will send message 'Sample msg' every minute starting from the given date and hour.
### !list
Lists all of the remembered reminders. Notation:
[{id}] Next event takes place: {date and hou}r, Is recurring: {Is it reccuring}, Reccuring in: {increment}.
MSG: {message}.
### !delete
#### Required positional parameters
* id - ID of the trigger for removal.
#### Example command
```bash
!delete 1
```
