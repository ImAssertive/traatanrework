import discord, asyncio, sys, traceback, checks, asyncpg, useful, credentialsFile
from discord.ext import commands

# def getPrefix(bot, message):
#     prefixes = ["re!"]
#     return commands.when_mentioned_or(*prefixes)(bot, message)
async def get_pre(bot, ctx):
    prefixes = []
    query = "SELECT * FROM Guilds WHERE guildid = $1 AND prefix IS NOT NULL"
    result = await bot.db.fetchrow(query, ctx.guild.id)
    if result:
        prefixes.append(result["prefix"])
    query = "SELECT * FROM Users WHERE userid = $1 AND prefix IS NOT NULL"
    result = await bot.db.fetchrow(query, ctx.author.id)
    if result:
        prefixes.append(result["prefix"])
    if prefixes == []:
        prefixes = "tt!"
    return prefixes


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


    @commands.command(name='help')
    @checks.is_not_banned()
    @checks.channel_is_enabled()
    async def help(self, ctx, command=None):
        embed = discord.Embed(title="UNNAMEDBOT Help Menu", colour=self.bot.getcolour())
        query = "SELECT * FROM Commands"
        results = await ctx.bot.db.fetch(query)
        if command != None:
            found = False
            for result in results:
                if commandname.lower() == result["name"] or (commandname.lower() in result["aliases"].split(", ") and result["aliases"].split(", ") != "No aliases!"):
                    found = True
                    embed.add_field(name="Command Name", value=result["name"])
                    embed.add_field(name="Command Aliases", value=result["aliases"])
                    embed.add_field(name="Required Permission", value=result["perm"])
                    if result["canbedisabled"]:
                        embed.add_field(name="Command Disable", value="This command can be disabled.")
                    else:
                        embed.add_field(name="Command Disable", value="This command can not be disabled.")
                    embed.add_field(name="Info", value=result["infotext"])
                    embed.add_field(name="Usage", value=result["usagetext"])
                    embed.add_field(name="Example", value=result["exampletext"])
            if not found:
                await ctx.channel.send(":no_entry: | Command not found! Use tt!help for a list of commands.")
        else:
            adminCommands = []
            miscCommands = []
            for result in results:
                if result["category"] == "Administration":
                    adminCommands.append(result["name"])
                elif result["category"] == "Miscellaneous":
                    miscCommands.append(result["name"])
            adminCommands = ', '.join(adminCommands)
            miscCommands = ', '.join(miscCommands)
            embed.add_field(name="Administration", value=adminCommands)
            embed.add_field(name="Miscellaneous", value=miscCommands)
        await ctx.channel.send(embed=embed)



    async def on_ready(self):
        print("Username: {0}\nID: {0.id}".format(self.user))
        game = discord.Game("chess with Rainbow Restarter!")
        await self.change_presence(status=discord.Status.online, activity=game)
        self.remove_command("help")

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