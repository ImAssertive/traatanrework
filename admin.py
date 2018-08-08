import discord, asyncio, sys, traceback, checks, useful, asyncpg, random
from discord.ext import commands

class adminCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setbantext')
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild", "setbantext")
    async def setbantext(self, ctx, *, banText):
        await csql.update("Guilds", "bantext", "banText", "guildID", str(ctx.guild.id))
        await ctx.channel.send(":white_check_mark: | Ban text set to `"+banText+"`!")

    @commands.command(name="setleave", aliases=['setfarewell', 'setleavechannel', 'setfarewellchannel'])
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild", "setleavechannel")
    async def setleave(self, ctx):
        await csql.update("Guilds", "leavechannel", str(ctx.channel.id), "guildID", str(ctx.guild.id))
        await ctx.channel.send(":white_check_mark: | Done! Farewell channel set here.")

    @commands.command(name="setwelcome", aliases=['setwelcomechannel'])
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild", "setwelcomechannel")
    async def setwelcome(self, ctx):
        await csql.update("Guilds", "welcomechannel", str(ctx.channel.id), "guildID", str(ctx.guild.id))
        await ctx.channel.send(":white_check_mark: | Done! Welcome channel set here.")

    @commands.command()
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild", "setwelcometext")
    async def setwelcometext(self, ctx, *, welcometext):
        await csql.update("Guilds", "welcometext", welcometext, "guildID", str(ctx.guild.id))
        await ctx.channel.send("Done! Welcome text set to ```" + welcometext + "```")

    @commands.command()
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild", "setleavetext")
    async def setfarewelltext(self, ctx, *, leavetext):
        await csql.update("Guilds", "leavetext", leavetext, "guildID", str(ctx.guild.id))
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
    async def ban(self, ctx, member, *, reason = None):
        kickban = "ban"
        await self.bankickFunction(ctx, member, reason, kickban)

    @commands.command()
    @checks.is_not_banned()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member, *, reason = None):
        kickban = "kick"
        await self.bankickFunction(ctx, member, reason, kickban)

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
            await ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** The reset command has closed due to inactivity.")
        else:
            if msg.content == str(confirmationnumber):
                embed = discord.Embed(title=":exclamation: | You have been "+ kickedbanned +" from " + ctx.guild.name,description="You have been "+ kickedbanned +" from " + ctx.guild.name + ". Details of this ban are listed below.",colour=self.bot.getcolour())
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
                await ctx.channel.send(":white_check_mark: | Canceled!")
                await baninfo.delete()

    @commands.command(name="enablecommand", aliases=['enable'])
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild","togglecommand")
    async def enablecommand(self, ctx, *, commandname):
        enableddisabled = "enabled"
        await self.commandToggleFunction(ctx, commandname, enableddisabled)

    @commands.command(name="disablecommand", aliases=['disable'])
    @checks.is_not_banned()
    @checks.has_permission_or_role("manage_guild","togglecommand")
    async def disablecommand(self, ctx, *, commandname):
        enableddisabled = "disabled"
        await self.commandToggleFunction(ctx, commandname, enableddisabled)

    async def commandToggleFunction(self, ctx, commandname, enableddisabled):
        query = "SELECT * FROM Commands"
        results = await ctx.bot.db.fetch(query)
        for result in results:
            if commandname.lower() == result["name"] or commandname.lower() in result["aliases"].split(", "):
                connection = await ctx.bot.db.acquire()
                async with connection.transaction():
                    if enableddisabled == "enabled":
                        query = "UPDATE GuildCommands SET enabled = true WHERE commandID = $1 AND guildID = $2"
                    elif enableddisabled == "disabled":
                        query = "UPDATE GuildCommands SET enabled = false WHERE commandID = $1 AND guildID = $2"
                    await ctx.bot.db.execute(query, result["commandID"], ctx.guild.id)
                await ctx.bot.db.release(connection)
                await ctx.channel.send(":white_check_mark: | **"+enableddisabled.title()+"** the **"+commandname+"** command.")
                break
        await ctx.channel.send(":no_entry: | Command not found.")

    async def test1(self, ctx):
        await ctx.channel.send(":white_check_mark:")

    @commands.command()
    @checks.is_not_banned()
    @commands.has_permissions(manage_guild = True)
    async def nsfw(self, ctx):
        options = []
        titleText = "NSFW Command Menu"
        if ctx.channel.is_nsfw():
            options.append([["Disable NSFW Commands","ctx.bot.cogs['adminCog'].test1(ctx)"],["0","disable"]])
        else:
            options.append([["Enable NSFW Commands","ctx.bot.cogs['adminCog'].test1(ctx)"],["0","enable"]])
        options.append([["List NSFW Channels", "ctx.bot.cogs['adminCog'].test1(ctx)"], ["1","list"]])
        footerText = "Current Channel: " + ctx.channel.name + " (" + str(ctx.channel.id) + ")"
        await useful.menuFunction(ctx, titleText, options, footerText)




def setup(bot):
    bot.add_cog(adminCog(bot))