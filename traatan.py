import discord, asyncio, sys, traceback, checks, asyncpg, useful, credentialsFile
from discord.ext import commands

# def getPrefix(bot, message):
#     self.prefixes = ["re!"]
#     return commands.when_mentioned_or(*self.prefixes)(bot, message)
async def get_pre(bot, ctx):
    pref = []
    guildDefault = True
    for each in bot.prefixes:
        if each[0] == ctx.guild.id:
            pref.append(each[1])
            guildDefault = False
        elif each[0] == ctx.author.id:
            pref.append(each[1])
    if guildDefault == True:
        pref.append("tt!")
    return pref


async def run():
    description = "Assertive's new bot. Please remind them to change this text if you see it."
    credentials = credentialsFile.getCredentials()
    db = await asyncpg.create_pool(**credentials)
    await db.execute('''CREATE TABLE IF NOT EXISTS Users(userID bigint PRIMARY KEY,
    xp bigint DEFAULT 0,
    backgroundimg text,
    prefix text,
    rep bigint DEFAULT 0,
    infotext text,
    titletext text,
    warncount bigint DEFAULT 0,
    bannedcount bigint DEFAULT 0,
    linkcount bigint DEFAULT 0,
    banned boolean DEFAULT false);
    
    CREATE TABLE IF NOT EXISTS Guilds(guildID bigint PRIMARY KEY,
    prefix text,
    raidroleid bigint,
    joinroleid bigint,
    kicktext text,
    bantext text,
    pubquiztime smallint DEFAULT 10, 
    ongoingpubquiz boolean DEFAULT false,
    pubquiztext text,
    pubquizendtext text DEFAULT 0,
    pubquizchannel bigint DEFAULT 0,
    pubquizquestionuserid bigint DEFAULT 0,
    pubquizquestionnumber integer DEFAULT 0,
    pubquizquestionactive boolean DEFAULT false,
    pubquizlastquestionsuper boolean DEFAULT false,
    welcomeChannel bigint,
    welcomeText text,
    welcome boolean DEFAULT false,
    leaveChannel bigint,
    leaveText text,
    leave boolean DEFAULT false,
    banned boolean DEFAULT false);
    
    CREATE TABLE IF NOT EXISTS Commands(commandID serial PRIMARY KEY,
    name text,
    perm text,
    aliases text,
    infotext text,
    usagetext text,
    exampletext text,
    gifurl text,
    category text,
    canbedisabled boolean);
    
    CREATE TABLE IF NOT EXISTS Channels(channelid bigint PRIMARY KEY,
    enabled boolean DEFAULT false);
    
    CREATE TABLE IF NOT EXISTS Roles(roleID bigint PRIMARY KEY,
    guildID bigint references Guilds(guildID) ON DELETE CASCADE ON UPDATE CASCADE,
    quizmaster boolean DEFAULT false,
    bluetext boolean DEFAULT false,
    togglecommand boolean DEFAULT false,
    bluetextcode boolean DEFAULT false,
    setWelcomeChannel boolean DEFAULT false,
    setWelcomeText boolean DEFAULT false,
    setLeaveChannel boolean DEFAULT false,
    setLeaveText boolean DEFAULT false,
    toggleRaid boolean DEFAULT false,
    setRaidRole boolean DEFAULT false,
    setRaidText boolean DEFAULT false,
    mute boolean DEFAULT false,
    cute boolean DEFAULT false,
    conch boolean DEFAULT false,
    eightball boolean DEFAULT false, 
    setMuteRole boolean DEFAULT false,
    esix boolean DEFAULT false,
    setbantext boolean DEFAULT false,
    setkicktext boolean DEFAULT false,
    selfAssignable boolean DEFAULT false);
      
    CREATE TABLE IF NOT EXISTS GuildCommands(guildID bigint references Guilds(guildID) ON DELETE CASCADE ON UPDATE CASCADE,
    commandID bigint references Commands(commandID) ON DELETE CASCADE ON UPDATE CASCADE,
    enabled boolean,
    PRIMARY KEY(guildID, commandID));
        
    CREATE TABLE IF NOT EXISTS GuildUsers(userID bigint references Users(userID) ON DELETE CASCADE ON UPDATE CASCADE,
    guildID bigint references Guilds(guildID) ON DELETE CASCADE ON UPDATE CASCADE,
    localxp integer DEFAULT 0,
    pubquizScoreTotal integer DEFAULT 0,
    pubquizScoreWeekly integer DEFAULT 0,
    PRIMARY KEY(userID, guildID));''')


    bot = Bot(description=description, db=db)
    bot.remove_command("help")
    initial_extensions = ['admin', 'setup', 'misc', 'justme']
    if __name__ == '__main__':
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print('Failed to load extension ' + extension, file=sys.stderr)
                traceback.print_exc()
    try:
        await bot.start(credentialsFile.getToken())
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            description=kwargs.pop("description"),
            command_prefix=get_pre
        )

        #self.pubquizAnswers = []
        self.db = kwargs.pop("db")
        self.currentColour = -1
        self.outcomes = ["It is certain", "It is decidedly so", "Without a doubt", "Yes - definitely",
                    "You may rely on it",
                    "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes",
                    "Reply hazy, try again", "Ask again later", "Better not tell you now",
                    "Cannot predict now", "Concentrate and ask again", "Don't count on it",
                    "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]


    async def on_ready(self):
        print("Username: {0}\nID: {0.id}".format(self.user))
        game = discord.Game("chess with Rainbow Restarter!")
        await self.change_presence(status=discord.Status.online, activity=game)
        self.prefixes = []
        query = "SELECT * FROM Guilds WHERE prefix IS NOT NULL"
        results = await self.db.fetch(query)
        if results:
            for result in results:
                self.prefixes.append([result["guildid"], result["prefix"]])
        query = "SELECT * FROM Users WHERE prefix IS NOT NULL"
        results = await self.db.fetch(query)
        if results:
            for result in results:
                self.prefixes.append([result["userid"], result["prefix"]])

    def getcolour(self):
        colours = ["5C6BC0", "AB47BC", "EF5350", "FFA726", "FFEE58", "66BB6A", "5BCEFA", "F5A9B8", "FFFFFF", "F5A9B8", "5BCEFA"]
        self.currentColour += 1
        if self.currentColour ==  len(colours):
            self.currentColour = 0
        return discord.Colour(int(colours[self.currentColour], 16))

    def conchcolour(self, number):
        if number < 10 and number > -1:
            return discord.Colour(int("00FF00", 16))
        elif number > 9 and number < 15:
            return discord.Colour(int("FFFF00", 16))
        else:
            return discord.Colour(int("FF0000", 16))

loop = asyncio.get_event_loop()
loop.run_until_complete(run())