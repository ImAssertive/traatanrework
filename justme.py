import discord, asyncio, sys, traceback, checks, useful, asyncpg, random, csql
from discord.ext import commands

class justmeCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.justme()
    async def setgame(self, ctx, *, gameName):
        game = discord.Game(gameName)
        await self.bot.change_presence(status=discord.Status.online, activity=game)
        await ctx.channel.send(":white_check_mark: | Online status set to: ** playing "+ gameName+"**")


    @commands.command(name='botglobalban', aliases=['bgb', 'fuckoff'], hidden = True)
    @checks.justme()
    async def botglobalban(self, ctx, member):
        memberid = int(useful.getid(member))
        await csql.update("Users","banned", "true", "userID", str(memberid))
        await ctx.channel.send(":white_check_mark: | Banned user **<@" + str(memberid) + ">** from all bot commands.")

    @commands.command(name='botglobalunban', aliases=['bgub', 'wback'], hidden = True)
    @checks.justme()
    async def botglobalunban(self, ctx, member):
        memberid = int(useful.getid(member))
        await csql.update("Users","banned", "false", "userID", str(memberid))
        await ctx.channel.send(":white_check_mark: | Unbanned user **<@" + str(memberid) + ">** from all bot commands.")

    @commands.command()
    @checks.justme()
    async def printevalquery(self, ctx, *, query):
        result = await ctx.bot.db.fetch(query)
        await ctx.channel.send(str(result))

    @commands.command()
    @checks.justme()
    async def echo(self, ctx, *, texttoecho):
        await ctx.channel.send(texttoecho)

    @commands.command()
    @checks.justme()
    async def evalquery(self, ctx, *, query):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            try:
                await self.bot.db.execute(query)
                await ctx.channel.send(":white_check_mark: | Done!")
            except:
                await ctx.channel.send(":no_entry: | An error occurred.")
        await self.bot.db.release(connection)

def setup(bot):
    bot.add_cog(justmeCog(bot))