import discord, asyncio, sys, traceback, checks, useful, asyncpg, random, csql
from discord.ext import commands

class adminCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setbantext', aliases=['setban'])
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild", "setbantext")
    @checks.command_is_enabled(14)
    @checks.channel_is_enabled()
    async def setbantext(self, ctx, *, banText="None"):
        await csql.update(ctx, "Guilds", "bantext", banText, "guildID", ctx.guild.id)
        await ctx.channel.send(":white_check_mark: | Ban text set to: ```"+banText+"```")

    @commands.command(name='setkicktext', aliases=['setkick'])
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild", "setkicktext")
    @commands.guild_only()
    @checks.command_is_enabled(15)
    @checks.channel_is_enabled()
    async def setkicktext(self, ctx, *, kickText="None"):
        await csql.update(ctx, "Guilds", "kicktext", kickText, "guildID", ctx.guild.id)
        await ctx.channel.send(":white_check_mark: | Kick text set to: ```"+kickText+"```")


    @commands.command(name='help')
    @checks.is_not_banned()
    @checks.channel_is_enabled()
    async def help(self, ctx, commandname=None):
        embed = discord.Embed(title="UNNAMEDBOT Help Menu", description="Use tt!help <COMMAND> for more information on a command. E.G. `tt!help kick`", colour=self.bot.getcolour())
        query = "SELECT * FROM Commands"
        results = await ctx.bot.db.fetch(query)
        if commandname != None:
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
            #embed.add_field(name="Miscellaneous", value=miscCommands)
        await ctx.channel.send(embed=embed)


    @commands.command(name='setprefix', aliases=['prefix', 'customprefix'])
    @checks.is_not_banned()
    @commands.guild_only()
    async def setprefix(self, ctx, *, enteredprefix):
        options = []
        if ctx.author.guild_permissions.manage_guild:
            titleText = "Prefix Command Menu"
            options.append([["Set prefix for guild","ctx.bot.cogs['adminCog'].prefixGuildMenu(ctx, kwargs)"],["0","guild","server"]])
            options.append([["Set prefix for just me","ctx.bot.cogs['adminCog'].prefixPersonalMenu(ctx, kwargs)"],["1","me","personal"]])
            footerText = "Current Guild: " + ctx.guild.name + " (" + str(ctx.guild.id) + ")   Selected Prefix: (" + enteredprefix + ")"
            descriptionText = "Options:\n"
            await useful.menuFunction(ctx, titleText, descriptionText, options, footerText, 60.0, prefix=enteredprefix)
        else:
            await self.prefixPersonalMenu(ctx, enteredprefix)

    async def prefixGuildMenu(self, ctx, kwargsDict):
        prefix = kwargsDict["prefix"]
        found == False
        await csql.update(ctx, "Guilds", "prefix", prefix, "guildID", ctx.guild.id)
        await ctx.channel.send(":white_check_mark: | Set prefix for **"+ ctx.guild.name +"** to `"+ prefix +"`.")
        print(ctx.bot.prefixes)
        for each in ctx.bot.prefixes:
            if each[0] == ctx.guild.id:
                each[1] = prefix
                found = True
            if found == False:
                ctx.bot.prefixes.append([ctx.guild.id, prefix])
    async def prefixPersonalMenu(self, ctx, prefix):
        if isinstance(prefix, dict):
            prefix = prefix["prefix"]
        await csql.update(ctx, "Users", "prefix", prefix, "userID", ctx.author.id)
        await ctx.channel.send(":white_check_mark: | Set prefix for **"+ ctx.author.name +"** to `"+ prefix +"`.")
        found = False
        for each in ctx.bot.prefixes:
            if each[0] == ctx.author.id:
                each[1] == prefix
                found = True
            if found == False:
                ctx.bot.prefixes.append([ctx.author.id, prefix])



    @commands.command(name="setleave", aliases=['setfarewell', 'setleavechannel', 'setfarewellchannel'])
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild", "setleavechannel")
    @commands.guild_only()
    @checks.command_is_enabled(11)
    @checks.channel_is_enabled()
    async def setleave(self, ctx, channel=None):
        if channel == None:
            await csql.update(ctx, "Guilds", "leavechannel", ctx.channel.id, "guildID", ctx.guild.id)
            await ctx.channel.send(":white_check_mark: | Done! Farewell channel set here.")
        elif ctx.message.channel_mentions==[]:
            await ctx.channel.send(":no_entry: | Channel not found! Do I have the `Read Messages` permission in the mentioned channel?")
        else:
            await csql.update(ctx, "Guilds", "leavechannel", ctx.message.channel_mentions[0].id, "guildID", ctx.guild.id)
            await ctx.channel.send(":white_check_mark: | Done! Farewell channel set to **"+ctx.message.channel_mentions[0].name+"**.")


    @commands.command(name="setwelcome", aliases=['setwelcomechannel'])
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild", "setwelcomechannel")
    @commands.guild_only()
    @checks.command_is_enabled(10)
    @checks.channel_is_enabled()
    async def setwelcome(self, ctx, channel=None):
        if channel == None:
            await csql.update(ctx, "Guilds", "welcomechannel", ctx.channel.id, "guildid", ctx.guild.id)
            await ctx.channel.send(":white_check_mark: | Done! Welcome channel set here.")
        elif ctx.message.channel_mentions==[]:
            await ctx.channel.send(":no_entry: | Channel not found! Do I have the `Read Messages` permission in the mentioned channel?")
        else:
            await csql.update(ctx, "Guilds", "welcomechannel", ctx.message.channel_mentions[0].id, "guildID", ctx.guild.id)
            await ctx.channel.send(":white_check_mark: | Done! welcomechannel channel set to **" + ctx.message.channel_mentions[0].name + "**.")

    @commands.command()
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild", "setwelcometext")
    @commands.guild_only()
    @checks.command_is_enabled(12)
    async def setwelcometext(self, ctx, *, welcometext):
        await csql.update(ctx, "Guilds", "welcometext", welcometext, "guildID", ctx.guild.id)
        await ctx.channel.send(":white_check_mark: | Done! Welcome text set to: ```" + welcometext + "```")

    @commands.command(name='setleavetext', aliases=['setfarewelltext'])
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild", "setleavetext")
    @commands.guild_only()
    @checks.command_is_enabled(13)
    @checks.channel_is_enabled()
    async def setleavetext(self, ctx, *, leavetext):
        await csql.update(ctx, "Guilds", "leavetext", leavetext, "guildID", ctx.guild.id)
        await ctx.channel.send("Done! Farewell text set to: ```" + leavetext + "```")

    @commands.command()
    async def gdpr(self, ctx):
        finished = 0
        successful = True
        while finished == 0:
            try:
                await ctx.author.send("Here is the data currently stored about you:")
            except:
                await ctx.channel.send("Please enable 'Allow direct messages from server members' under 'Privacy & Safety' in settings. For security reasons this information can not be posted publicly.")
                successful = False
                break
            embed = discord.Embed(title="Global Data:", description="", colour=self.bot.getcolour())
            query = "SELECT * FROM Users WHERE userID = $1"
            results = await ctx.bot.db.fetchrow(query, ctx.author.id)
            if results:
                embed.add_field(name="Your user ID is: ", value=("{}".format(results["userid"])))
                embed.add_field(name="You are pubquizDM settings are currently:", value=("{}".format(results["pubquizdm"])))
                embed.add_field(name="Your global banned status is currently:", value=("{}".format(results["banned"])))
            else:
                embed = discord.Embed(title="Global Data:", description="No data found!", colour=self.bot.getcolour())
            await ctx.author.send(embed=embed)
            query = "SELECT * FROM GuildUsers WHERE userID = $1"
            results = await ctx.bot.db.fetch(query, ctx.author.id)
            if results:
                embed = discord.Embed(title="Server Data:", description="", colour=self.bot.getcolour())
                for row in results:
                    currentRow = row
                    embed.add_field(name="The following information is for guild ID:", value=("{}".format(currentRow["guildid"])), inline=False)
                    embed.add_field(name="Your Total Pub Quiz Score is:", value=("{}".format(currentRow["pubquizscoretotal"])), inline=False)
                    embed.add_field(name="Last Pub Quiz your score was:", value=("{}".format(currentRow["pubquizscoreweekly"])), inline=False)
                    embed.add_field(name="Your banned status here is:", value=("{}".format(currentRow["banned"])), inline=False)
            else:
                embed = discord.Embed(title="Server Data:", description="No data found!", colour=self.bot.getcolour())
            await ctx.author.send(embed=embed)
            query = "SELECT * FROM UserGameAccounts WHERE userID = $1"
            results = await ctx.bot.db.fetch(query, ctx.author.id)
            if results:
                for row in results:
                    currentRow = row
                embed = discord.Embed(title="Im still working on this bit!", description="You should never see this! If you do, contact @Zootopia#0001 for this information.")
            else:
                embed = discord.Embed(title="Game account data:", description="No data found!")
            await ctx.author.send(embed = embed)
            finished = 1
        if successful:
            await ctx.channel.send(":white_check_mark: | Information sent to DM!")

    @commands.command()
    @checks.is_not_banned()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @checks.command_is_enabled(2)
    @checks.channel_is_enabled()
    async def ban(self, ctx, member, *, reason = None):
        kickban = "ban"
        await self.bankickFunction(ctx, member, kickban, reason)

    @commands.command()
    @checks.is_not_banned()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @checks.command_is_enabled(16)
    @checks.channel_is_enabled()
    async def hackban(self, ctx, memberid):
        try:
            await ctx.guild.ban(discord.Object(id=int(memberid)))
            await ctx.channel.send(":white_check_mark: | Banned ID `"+str(memberid)+"`")
        except:
            await ctx.channel.send(":no_entry: | An error occurred. Was that a valid user ID?")

    @commands.command()
    @checks.is_not_banned()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    @checks.command_is_enabled(1)
    @checks.channel_is_enabled()
    async def kick(self, ctx, member, *, reason = None):
        kickban = "kick"
        await self.bankickFunction(ctx, member, kickban, reason)

    async def bankickFunction(self, ctx, member, kickban, reason = None):
        memberid = ctx.message.mentions[0].id
        if kickban == "kick":
            kickedbanned = "kicked"
            kickingbanning = "kicking"
            texttosend = "kicktext"
        elif kickban == "ban":
            kickedbanned = "banned"
            kickingbanning = "banning"
            texttosend = "bantext"
        confirmationnumber = random.randint(1000, 9999)
        embed = discord.Embed(title="You are about to "+kickban+" user: " + ctx.message.mentions[0].display_name, description="This action is irreversable. To continue please type `" + str(confirmationnumber) + "` or to cancel, please type `cancel`.",colour=self.bot.getcolour())
        embed.add_field(name='User ID: ', value=str(ctx.message.mentions[0].id), inline=False)
        embed.add_field(name='User discord name: ',value=ctx.message.mentions[0].name + "#" + ctx.message.mentions[0].discriminator,inline=False)
        if reason:
            embed.add_field(name='Reason: ', value=reason, inline=False)
        else:
            embed.add_field(name='Reason: ', value="None given.", inline=False)
        baninfo = await ctx.channel.send(embed=embed)
        def confirmationcheck(msg):
            return (msg.content == str(confirmationnumber) or msg.content.lower() == "cancel") and ctx.channel.id == msg.channel.id and msg.author.id == ctx.author.id
        try:
            msg = await self.bot.wait_for('message', check=confirmationcheck, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** The menu has closed due to inactivity.")
        else:
            if msg.content == str(confirmationnumber):
                embed = discord.Embed(title=":exclamation: | You have been "+ kickedbanned +" from " + ctx.guild.name,description="You have been "+ kickedbanned +" from " + ctx.guild.name + ". Details of this "+kickban+" are listed below.",colour=self.bot.getcolour())
                embed.add_field(name="User (You):", value=ctx.message.mentions[0].mention + " " + ctx.message.mentions[0].name + "#" + ctx.message.mentions[0].discriminator + " `" + str(ctx.message.mentions[0].id) + "`", inline=False)
                embed.add_field(name="Issued by:", value=ctx.author.mention + " " + ctx.author.name + "#" + ctx.author.discriminator + " `" + str(ctx.author.id) + "`", inline=False)
                if reason:
                    embed.add_field(name='Reason: ', value=reason, inline=False)
                else:
                    embed.add_field(name='Reason: ', value="None given.", inline=False)
                query = "SELECT * FROM guilds WHERE guildID = $1 AND "+texttosend+" IS NOT NULL"
                results = await ctx.bot.db.fetchrow(query, ctx.guild.id)
                if results:
                    embed.add_field(name="Message from server:", value=results[texttosend])
                await ctx.channel.send(":white_check_mark: | "+kickingbanning.title()+" user...")
                await ctx.message.mentions[0].send(embed=embed)
                if reason:
                    if kickban == "kick":
                        await ctx.message.mentions[0].kick(reason=reason)
                    elif kickban == "ban":
                        await ctx.message.mentions[0].ban(reason=reason)
                else:
                    if kickban == "kick":
                        await ctx.message.mentions[0].kick(reason="None given.")
                    elif kickban == "ban":
                        await ctx.message.mentions[0].ban(reason="None given.")
            elif msg.content.lower() == "cancel":
                canceledtext = await ctx.channel.send(":white_check_mark: | Canceled!")
                await baninfo.delete()
                await asyncio.sleep(2)
                await canceledtext.delete()

    @commands.command(name="enablecommand", aliases=['enable'])
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild","togglecommand")
    @commands.guild_only()
    async def enablecommand(self, ctx, *, commandname=None):
        if ctx.message.channel_mentions != []:
            enabledisable = "enable"
            channel = str(ctx.message.channel_mentions[0].id)
            await self.toggleChannelFunction(ctx, enabledisable, channel)
        elif commandname == None:
            enabledisable = "enable"
            await self.toggleChannelFunction(ctx, enabledisable)
        else:
            enableddisabled = "enabled"
            await self.commandToggleFunction(ctx, commandname, enableddisabled)

    @commands.command(name="disablecommand", aliases=['disable'])
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild","togglecommand")
    @commands.guild_only()
    async def disablecommand(self, ctx, *, commandname=None):
        if ctx.message.channel_mentions != []:
            enabledisable = "disable"
            channel = str(ctx.message.channel_mentions[0].id)
            await self.toggleChannelFunction(ctx, enabledisable, channel)
        elif commandname == None:
            enabledisable = "disable"
            await self.toggleChannelFunction(ctx, enabledisable)
        else:
            enableddisabled = "disabled"
            await self.commandToggleFunction(ctx, commandname, enableddisabled)

    async def commandToggleFunction(self, ctx, commandname, enableddisabled):
        query = "SELECT * FROM Commands"
        results = await ctx.bot.db.fetch(query)
        for result in results:
            if commandname.lower() == result["name"] or (commandname.lower() in result["aliases"].split(", ") and result["aliases"].split(", ") != "No aliases!"):
                query = "SELECT * FROM GuildCommands WHERE commandid = $1 AND guildid = $2"
                commandresult = await ctx.bot.db.fetchrow(query, result["commandid"], ctx.guild.id)
                connection = await ctx.bot.db.acquire()
                async with connection.transaction():
                    if commandresult == None:
                        query = "INSERT INTO GuildCommands(guildid, commandid) VALUES ($1, $2)"
                        await ctx.bot.db.execute(query, ctx.guild.id, result["commandid"])
                    if enableddisabled == "enabled":
                        query = "UPDATE GuildCommands SET enabled = true WHERE commandid = $1 AND guildid = $2"
                    elif enableddisabled == "disabled":
                        query = "UPDATE GuildCommands SET enabled = false WHERE commandid = $1 AND guildid = $2"
                    await ctx.bot.db.execute(query, result["commandid"], ctx.guild.id)
                await ctx.bot.db.release(connection)
                await ctx.channel.send(":white_check_mark: | **"+enableddisabled.title()+"** the **"+commandname+"** command.")
                return
        await ctx.channel.send(":no_entry: | Command not found.")

    @commands.command(name="listnsfw", aliases=['nsfwlist'])
    @checks.is_not_banned()
    @commands.guild_only()
    @checks.channel_is_enabled()
    @checks.command_is_enabled(9)
    async def listnsfw(self, ctx):
        totalcount = 0
        titleText = "NSFW Command Menu"
        descriptionText = "The following channels have NSFW permissions:\n"
        for channel in ctx.guild.text_channels:
            if channel.is_nsfw():
                totalcount += 1
                descriptionText += "\n" + str(totalcount) +": " + channel.name
        await useful.menuFunction(ctx, titleText, descriptionText)

    @commands.command(name="nsfw", aliases=['togglensfw', 'setnsfw'])
    @checks.is_not_banned()
    @commands.has_permissions(manage_guild = True)
    @commands.guild_only()
    @checks.channel_is_enabled()
    @checks.command_is_enabled(8)
    async def nsfw(self, ctx, channel=None):
        if ctx.channel.is_nsfw() and channel == None:
            await ctx.channel.send(":white_check_mark: | This channel is no longer NSFW.")
            await ctx.channel.edit(nsfw=False, reason="Requested by: "+ctx.message.author.name + "#" + ctx.message.author.discriminator + " (" + str(ctx.message.author.id)+").")
        elif (not ctx.channel.is_nsfw()) and channel == None:
            await ctx.channel.send(":white_check_mark: | This channel is now an NSFW channel.")
            await ctx.channel.edit(nsfw=True, reason="Requested by: "+ctx.message.author.name + "#" + ctx.message.author.discriminator + " (" + str(ctx.message.author.id)+").")
        elif channel != None:
            if ctx.message.channel_mentions == []:
                await ctx.channel.send(":no_entry: | Channel not found! Do I have the `Read Messages` permission in the mentioned channel?")
                return
            else:
                channelid = ctx.message.channel_mentions[0].id
                if ctx.guild.get_channel(channelid) != None:
                    if ctx.guild.get_channel(channelid).is_nsfw():
                        ctx.guild.get_channel(channelid).edit(nsfw=False, reason="Requested by: "+ctx.message.author.name + "#" + ctx.message.author.discriminator + " (" + str(ctx.message.author.id)+").")
                        await ctx.channel.send(":white_check_mark: | **"+ctx.guild.get_channel(channelid).name+"** is no longer an NSFW channel.")
                    else:
                        ctx.guild.get_channel(channelid).edit(nsfw=True, reason="Requested by: "+ctx.message.author.name + "#" + ctx.message.author.discriminator + " (" + str(ctx.message.author.id)+").")
                        await ctx.channel.send(":white_check_mark: | **"+ctx.guild.get_channel(channelid).name+"** is now an NSFW channel.")
                else:
                    await ctx.channel.send(":no_entry: | Channel not found! Do I have the `Read Messages` permission in the mentioned channel?")

    @commands.command(name="enablechannel", aliases =['unignorechannel', 'unignore'])
    @checks.is_not_banned()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def enablechannel(self, ctx, channel=None):
        enabledisable = "enable"
        if channel:
            await self.toggleChannelFunction(ctx, enabledisable, channel)
        else:
            await self.toggleChannelFunction(ctx, enabledisable)

    @commands.command(name="disablechannel", aliases =['ignorechannel','ignore'])
    @checks.is_not_banned()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def disablechannel(self, ctx, channel=None):
        enabledisable = "disable"
        if channel:
            await self.toggleChannelFunction(ctx, enabledisable, channel)
        else:
            await self.toggleChannelFunction(ctx, enabledisable)


    async def toggleChannelFunction(self, ctx, enabledisable, channel=None):
        if channel == None:
            channelid = ctx.channel.id
        else:
            try:
                channelid = useful.getid(channel)
            except:
                await ctx.channel.send(":no_entry: | Channel not found! Do I have the `Read Messages` permission in the mentioned channel?")
                return
        if ctx.guild.get_channel(channelid) != None:
            if enabledisable == "enable":
                enableddisabled = "enabled"
                enabledisablebool = True
            else:
                enableddisabled = "disabled"
                enabledisablebool = False
            query = "SELECT * FROM Channels WHERE channelid = $1"
            result = await ctx.bot.db.fetchrow(query, channelid)
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                if result is None:
                    query = "INSERT INTO Channels (channelID) VALUES($1) ON CONFLICT DO NOTHING"
                    await self.bot.db.execute(query, channelid)
                query = "UPDATE Channels SET enabled = $1 WHERE channelid = $2"
                await self.bot.db.execute(query, enabledisablebool, channelid)
            await self.bot.db.release(connection)
            await ctx.channel.send(":white_check_mark: | Commands "+enableddisabled+" in **" +ctx.guild.get_channel(channelid).name+"**.")
        else:
            await ctx.channel.send(":no_entry: | Channel not found! Do I have the `Read Messages` permission in the mentioned channel?")


def setup(bot):
    bot.add_cog(adminCog(bot))