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
                    if "now" in args[i+1]:
                        splitted = args[i+1].split("+")
                        self.nextEvent = datetime.datetime.now()
                        if len(splitted) > 1:
                            delta = Trigger.getTimeDeltaFromString(splitted[1])
                            self.nextEvent = datetime.datetime.now()+delta
                    else:
                        self.nextEvent = datetime.datetime.strptime(args[i+1],"%d.%m.%y-%H:%M")
                if args[i].lower() == "-r":
                    self.recurring = True
                if args[i].lower() == "-i":
                    self._inc = Trigger.getTimeDeltaFromString(args[i+1])
                if args[i].lower() == "-m":
                    self.msg=args[i+1]
        else:
            raise Exception("Lack of required date+hour parameter.")

    def __str__(self):
        return "Next event takes place: {}, Is recurring: {}, Reccuring in: {}.\nMSG: {}".format(self.nextEvent,self.recurring,self._inc,self.msg)

    @staticmethod
    def getTimeDeltaFromString(str):
        if "s" in str.lower():
            return datetime.timedelta(seconds=int(str.lower().replace("s", "")))
        if "m" in str.lower():
            return datetime.timedelta(minutes=int(str.lower().replace("m", "")))
        if "h" in str.lower():
            return datetime.timedelta(hours=int(str.lower().replace("h", "")))
        if "d" in str.lower():
            return datetime.timedelta(days=int(str.lower().replace("d", "")))
        if "w" in str.lower():
            return datetime.timedelta(weeks=int(str.lower().replace("w", "")))


    async def trigger(self,ctx):
        await ctx.send(self.msg)
        if self.recurring:
            self.nextEvent = datetime.datetime.now()+self._inc
        else:
            self.dead = True

    async def shouldTrigger(self,ctx):
        if datetime.datetime.now()>self.nextEvent:
            await self.trigger(ctx)