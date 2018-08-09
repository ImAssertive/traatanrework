import discord, asyncio, sys, traceback, checks, asyncpg, useful, credentialsFile
from discord.ext import commands

# def getPrefix(bot, message):
#     prefixes = ["re!"]
#     return commands.when_mentioned_or(*prefixes)(bot, message)

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
    pubquizendtext text,
    pubquizchannel bigint,
    pubquizquestionuserid bigint,
    pubquizquestionnumber integer DEFAULT 0,
    pubquizquestionactive boolean DEFAULT false,
    pubquizlastquestionsuper boolean DEFAULT false,
    welcomeChannel bigint,
    welcomeText text,
    leaveChannel bigint,
    leaveText text,
    banned boolean DEFAULT false);
    
    CREATE TABLE IF NOT EXISTS Commands(commandID serial PRIMARY KEY,
    name text,
    perm text,
    aliases text,
    infotext text,
    usagetext text,
    exampletext text,
    gifurl text,
    canbedisabled boolean);
    
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

    async def get_prefix(bot, ctx):
        prefixes = []
        query = "SELECT * FROM Guilds WHERE guildid = $1 AND prefix IS NOT NULL"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            prefixes.append(result["prefix"])
        query = "SELECT * FROM Users WHERE userid = $1 AND prefix IS NOT NULL"
        result = await ctx.bot.db.fetchrow(query, ctx.author.id)
        if result:
            prefixes.append(result["prefix"])
        if prefixes == []:
            prefixes = "tt!"
        return prefixes

    bot = Bot(description=description, db=db, command_prefix=get_prefix(bot, ctx))
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