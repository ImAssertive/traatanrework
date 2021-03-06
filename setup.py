import discord, asyncio, sys, traceback, checks, useful, asyncpg, random
from discord.ext import commands


class setupCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "exit", aliases =['quit', 'kill'], hidden = True)
    @checks.justme()
    async def exit(self, ctx):
        thanos = random.randint(1,5)
        if thanos == 1:
            await ctx.channel.send("Mrs Assertive I dont feel so good...")
        if thanos == 2:
            await ctx.channel.send("Why...")
        if thanos == 3:
            await ctx.channel.send(":wave: Goodbye.")
        if thanos == 4:
            await ctx.channel.send("Faster, Bambi! Don't look back! Keep running! Keep running!")
        if thanos == 5:
            await ctx.channel.send("The horror. The horror.")
        await self.bot.db.close()
        await self.bot.logout()
        sys.exit()


    @commands.command(hidden = True)
    @checks.justme()
    async def addmembers(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            for member in ctx.guild.members:
                query = "INSERT INTO Users (userID) VALUES($1) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, member.id)
                query = "INSERT INTO GuildUsers (guildID, userID) VALUES($1, $2) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, ctx.guild.id, member.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")

    @commands.command(hidden = True)
    @checks.justme()
    async def addcommands(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Commands (aliases, commandid, name, perm, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, "No aliases!", 1, "kick", "kick_members", "Kicks the mentioned user. Can attatch an optional reason for the kick after the user mention.", "`tt!kick <@USER>` or `tt!kick <@USER> <Reason>`", "tt!kick @MrSpam#0001 Spamming in general.", True, "Administration")
            query = "INSERT INTO Commands (aliases, commandid, name, perm, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, "No aliases!", 2, "ban", "ban_members", "Bans the mentioned user. Can attatch an optional reason for the ban after the user mention.", "`tt!ban <@USER>` or `tt!ban <@USER> <Reason>`", "tt!ban @MrSpam#0001 Spamming in general.", True, "Administration")
            query = "INSERT INTO Commands (commandid, name, perm, aliases, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, 3, "enable", "manage_guild", "enablecommand", "Enables the specified command. Can be either channel or server wide. Excludes blacklisted channels.\nManagement commands can not be disabled", "`tt!enable CommandName`", "tt!enable Eightball", False, "Administration")
            query = "INSERT INTO Commands (commandid, name, perm, aliases, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, 4, "disable", "manage_guild", "disablecommand | ignorecommand", "Disables the specified command. Can be either channel or server wide. \nManagement commands can not be disabled", "tt!disable CommandName", "tt!disable Eightball", False, "Administration")
            query = "INSERT INTO Commands (commandid, name, perm, aliases, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, 5, "listcommands", "manage_guild", "commandslist", "Lists the enabled status of each command. ", "tt!disable CommandName", "tt!disable Eightball", False, "Administration")
            query = "INSERT INTO Commands (commandid, name, perm, aliases, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, 6, "disablechannel", "manage_guild", "ignorechannel | ignore", "Disables all commands in the specified channel. \nManagement commands can not be disabled", "`tt!disable <#CHANNEL>` or `tt!disable`", "tt!disable #General", False, "Administration")
            query = "INSERT INTO Commands (commandid, name, perm, aliases, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, 7, "enablechannel", "manage_guild", "unignorechannel | unignore", "Enables all commands in the specified channel. \nManagement commands can not be disabled.", "`tt!enable <#CHANNEL>` or `tt!enable`", "tt!enable #General", False, "Administration")
            query = "INSERT INTO Commands (commandid, name, perm, aliases, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, 8, "nsfw", "manage_guild", "togglensfw | setnsfw", "Toggles NSFW commands in the specified chat.", "`tt!nsfw <#CHANNEL>` or `tt!nsfw`", "tt!nsfw #General", False, "Administration")
            query = "INSERT INTO Commands (commandid, name, perm, aliases, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, 9, "listnsfw", "manage_guild", "nsfwlist", "Lists NSFW channels in the guild.", "`tt!listnsfw`", "tt!listnsfw", False, "Administration")
            query = "INSERT INTO Commands (commandid, name, perm, aliases, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, 10, "setwelcome", "manage_guild", "setwelcomechannel", "Sets the channel for a welcome message to be sent upon a user joining the server.", "`tt!setwelcome` or `tt!setwelcome <#CHANNEL>`", "tt!setwelcome #General", True, "Administration")
            query = "INSERT INTO Commands (commandid, name, perm, aliases, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, 11, "setleave", "manage_guild", "setleavechannel, setfarewellchannel, setfarewell", "Sets the channel for a farewell message to be sent upon a user leaving the server.", "`tt!setleave` or `tt!setleave <#CHANNEL>`", "tt!setleave #General", True, "Administration")
            query = "INSERT INTO Commands (commandid, name, perm, aliases, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, 12, "setwelcometext", "manage_guild", "No aliases", "Sets the welcome message to be sent upon a user joining the server. \n%NAME% will be replaced with the users name.\n%MENTION% will mention the user.\n%GUILD% will be replaced with the guild name.", "`tt!setwelcome <MESSAGE>`", "tt!setwelcometext Welcome %MENTION% to %GUILD%!", True, "Administration")
            query = "INSERT INTO Commands (commandid, name, perm, aliases, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, 13, "setleavetext", "manage_guild", "setfarewelltext", "Sets the farewell message to be sent upon a user leaving the server. \n%NAME% will be replaced with the users name.\n%MENTION% will mention the user.\n%GUILD% will be replaced with the guild name.", "`tt!setleave <MESSAGE>`", "tt!setleavetext %USER% has left %GUILD%! We hope to see you again soon.", True, "Administration")
            query = "INSERT INTO Commands (commandid, name, perm, aliases, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, 14, "setbantext", "manage_guild", "setban", "Sets the message to be sent to a user upon being banned.", "`tt!setbantext <MESSAGE>`", "tt!setbantext This ban is permanent. To appeal this ban please contact Moderator#0000.", True, "Administration")
            query = "INSERT INTO Commands (commandid, name, perm, aliases, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, 15, "setkicktext", "manage_guild", "setkick", "Sets the message to be sent to a user upon being kicked.", "`tt!setkicktext <MESSAGE>`", "tt!setkicktext You have been kicked. Please contact Moderator#0000 to be allowed back into the guild.", True, "Administration")
            query = "INSERT INTO Commands (aliases, commandid, name, perm, infotext, usagetext, exampletext, canbedisabled, category) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, "No aliases!", 16, "hackban", "ban_members", "Bans the mentioned user ID. Used against preventing spambots.", "`tt!hackban <ID>`", "tt!hackban 000000000000000000", True, "Administration")



        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")


    @commands.command(hidden= True)
    @checks.justme()
    async def addroles(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            for role in ctx.guild.roles:
                query = "INSERT INTO Roles (roleID, guildID) VALUES($1, $2) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, role.id, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")


    @commands.command(hidden = True)
    @checks.justme()
    async def addguild(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Guilds (guildID) VALUES($1) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")

    @commands.command(hidden = True)
    @checks.justme()
    async def deletemember(self, ctx, member):
        memberid = int(useful.getid(member))
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "DELETE FROM Users WHERE userID = $1"
            await self.bot.db.execute(query, memberid)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")


    async def on_guild_join(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Guilds (guildID) VALUES($1) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.id)
            for member in ctx.members:
                query = "INSERT INTO Users (userID) VALUES($1) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, member.id)
                query = "INSERT INTO GuildUsers (guildID, userID) VALUES($1, $2) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, ctx.id, member.id)
            for role in ctx.roles:
                query = "INSERT INTO Roles (roleID, guildID) VALUES($1, $2) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, role.id, ctx.id)
        await self.bot.db.release(connection)


    async def on_guild_role_create(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Roles (roleID, guildID) VALUES($1, $2) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.id, ctx.guild.id)
        await self.bot.db.release(connection)

    async def on_guild_role_delete(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "DELETE FROM Roles WHERE roleID = $1"
            await self.bot.db.execute(query, ctx.id)
        await self.bot.db.release(connection)

    async def on_guild_remove(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "DELETE FROM GuildUsers WHERE guildID = $1"
            await self.bot.db.execute(query, ctx.id)
            query = "DELETE FROM Guilds WHERE guildID = $1"
            await self.bot.db.execute(query, ctx.id)
            query = "DELETE FROM Roles WHERE guildID = $1"
            await self.bot.db.execute(query, ctx.id)
        await self.bot.db.release(connection)

    async def on_member_remove(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "DELETE FROM GuildUsers WHERE userID = $1 AND guildID = $2"
            await self.bot.db.execute(query, ctx.id, ctx.guild.id)
        await self.bot.db.release(connection)

        query = "SELECT * FROM Guilds WHERE guildID = $1 AND banned = false AND leave = true AND leavetext IS NOT NULL AND leavechannel IS NOT NULL"
        result = await self.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            channelID = (result["leavechannel"])
            leavetext = useful.formatTextLeave(ctx, result["leavetext"])
            await ctx.guild.get_channel(int(channelID)).send(leavetext)

    async def on_member_join(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Users (userID) VALUES($1) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.id)
            query = "INSERT INTO GuildUsers (guildID, userID) VALUES($1, $2) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.guild.id, ctx.id)
        await self.bot.db.release(connection)
        query = "SELECT * FROM Guilds WHERE guildID = $1 AND banned = false AND welcome = true AND welcometext IS NOT NULL AND welcomechannel IS NOT NULL"
        result = await self.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            channelID = ("{}".format(result["welcomechannel"]))
            welcometext = useful.formatText(ctx, ("{}".format(result["welcometext"])))
            await ctx.guild.get_channel(int(channelID)).send(welcometext)


    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.CommandNotFound):
    #         return
    #     elif isinstance(error, commands.CheckFailure):
    #         try:
    #             await ctx.channel.send(":no_entry: | You do not have permission for {} here.".format(ctx.command))
    #         except:
    #             pass




def setup(bot):
    bot.add_cog(setupCog(bot))