import datetime
class Trigger:
    def __init__(self, next:datetime.datetime, recurring:bool, increment:datetime.timedelta,msg:str):
        self.nextEvent = next
        self.recurring = recurring
        self._inc = increment
        self.msg = msg
        self.dead = False

    def __init__(self, args:[]):
        self.nextEvent = None
        self.recurring = None
        self._inc = None
        self.msg = None
        self.dead = False
        if "date+hour" in args:
            for i in range(len(args)):
                if args[i].lower() == "date+hour":
                    self.nextEvent = datetime.datetime.strptime(args[i+1],"%d.%m.%y-%H:%M")
                if args[i].lower() == "-r":
                    self.recurring = True
                if args[i].lower() == "-i":
                    if "m" in args[i+1].lower():
                        self._inc = datetime.timedelta(minutes=int(args[i+1].lower().replace("m","")))
                    if "d" in args[i + 1].lower():
                        self._inc = datetime.timedelta(days=int(args[i + 1].lower().replace("d", "")))
                    if "w" in args[i + 1].lower():
                        self._inc = datetime.timedelta(weeks=int(args[i + 1].lower().replace("w", "")))
                if args[i].lower() == "-m":
                    self.msg=args[i+1]
        else:
            raise Exception("Lack of required date+hour parameter.")

    def __str__(self):
        return "Next event takes place: {}, Is recurring: {}, Reccuring in: {}.\nMSG: {}".format(self.nextEvent,self.recurring,self._inc,self.msg)

    async def trigger(self,ctx):
        await ctx.send(self.msg)
        if self.recurring:
            self.nextEvent = datetime.datetime.now()+self._inc
        else:
            self.dead = True

    async def shouldTrigger(self,ctx):
        if datetime.datetime.now()>self.nextEvent:
            await self.trigger(ctx)