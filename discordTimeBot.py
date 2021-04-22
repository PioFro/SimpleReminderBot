from discord.ext import commands
import logging
import asyncio
from trigger import Trigger
import settings
import sys

class ReminderController:
    reminderContexts = []
    @staticmethod
    def addReminderContext(uid, ctx,tr:Trigger):
        for rs in ReminderController.reminderContexts:
            if rs._uqID == uid:
                rs.addTrigger(tr)
                return
        logging.info("Created new Sending context")
        ReminderController.reminderContexts.append(ReminderSender(ctx,uid,tr))
    @staticmethod
    async def run():
        while True:
            logging.info("Reminder Controller doing scan. ")
            for rs in ReminderController.reminderContexts:
                await rs.checkTriggers()
            await asyncio.sleep(settings.REFRESH_RATE)
    @staticmethod
    def getListForUid(uid:int):
        for rs in ReminderController.reminderContexts:
            if rs._uqID == uid:
                return str(rs)
    @staticmethod
    def deleteTrigger(uid, trigger):
        for rs in ReminderController.reminderContexts:
            if rs._uqID == uid:
                rs.delTrigger(int(trigger))


class ReminderSender:
    def __init__(self,c,uid:int, tr:Trigger):
        self.ctx = c
        self._uqID = uid
        self.triggers = []
        self.triggers.append(tr)

    def addTrigger(self, trigger:Trigger):
        self.triggers.append(trigger)

    def delTrigger(self, id):
        try:
            self.triggers.remove(self.triggers[id])
        except:
            logging.info("Tried to delete trigger that was not in the list")

    def __str__(self):
        ret = ""
        for i in range(len(self.triggers)):
            ret+="[{}]\t{}\n".format(i,str(self.triggers[i]))
        return ret

    async def checkTriggers(self):
        for trigger in self.triggers.copy():
            await trigger.shouldTrigger(self.ctx)
            if trigger.dead:
                self.triggers.remove(trigger)


logging.basicConfig(filename='bot.log', level=logging.DEBUG)
token = sys.argv[1]
bot = commands.Bot(command_prefix='!')
channel = None

@bot.event
async def on_ready():
    logging.info("Bot connected.")

@bot.command(name="add",help="Adds new reminder or recurring reminder. Use format date+hour dd.mm.yy-HH:MM (or now+(1-60)(s/m/h/d/w)) with optional "
                             "parameters: \n-r recurring \n-i interval of reccuring (ex. 1d = 1 day) - "
                             "possible intervals (s)econds, (w)eeks, (d)ay, (h)our, (m)inute\n-m Message to send.\nExample command: "
                             "!add date+hour 10.01.21-10:21 -m Sample msg -r -i 1m\nExample command will send message"
                             " 'Sample msg' every minute starting from the given date and hour.")
async def add(ctx,*args):
    logging.info("Received remainder.{}".format(args))
    try:
        tr = Trigger(args)
    except:
        logging.error("Wrong trigger information")
        await ctx.send("Wrong trigger - provide minimally trigger with !add date+hour dd.mm.yy-HH:MM")
        return
    ReminderController.addReminderContext(ctx.channel.id, ctx, tr)
    await ctx.send("Understood sire. I'll remind you "+str(tr))


@bot.command(name="list",help="Lists all of the remembered reminders.")
async def list(ctx):
    await ctx.send(ReminderController.getListForUid(ctx.channel.id))


@bot.command(name="delete",help="Deletes one reminder specified by the ID. To obtain ID list all of the reminders - "
                                "the id will be at the beginning of the line ([id] <reminder data>")
async def delete(ctx, id):
    ReminderController.deleteTrigger(ctx.channel.id, id)
    await ctx.send("Trigger {} was deleted.".format(id))

bot.loop.create_task(ReminderController.run())
bot.run(token)