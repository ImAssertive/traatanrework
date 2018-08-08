import discord
from discord.ext import commands

def has_role(*arg):
    async def predicate(ctx):
        for counter in range (0,len(arg)):
            if discord.utils.get(ctx.guild.roles, name=str(arg[counter])) in ctx.author.roles:
                return True
        return False
    return commands.check(predicate)

def has_permission_or_role(permLevel, command):
    async def predicate(ctx):
        print(permLevel, ctx.author.permissions_in(ctx.channel))
        if permLevel in ctx.author.permissions_in(ctx.channel):
            return True
        else:
            rolesData = await getRolePerms(ctx)
            for role in rolesData:
                if role[command] == True:
                    return True
            return False
    return commands.check(predicate)

def justme():
    async def predicate(ctx):
        if ctx.author.id == 163691476788838401 or ctx.author.id == 463103145845850122:
            return True
        else:
            return False
    return commands.check(predicate)

def is_not_banned():
    async def predicate(ctx):
        query = "SELECT * FROM Users WHERE userID = $1 AND banned = false"
        result = await ctx.bot.db.fetchrow(query, ctx.author.id)
        if result:
            return True
        return False
    return commands.check(predicate)

async def getRolePerms(ctx):
    roleIDs = []
    rolesdata = []
    for role in ctx.author.roles:
        roleIDs.append(role.id)
    for i in range(0, len(roleIDs)):
        query = "SELECT * FROM Roles WHERE roleID = $1"
        result = await ctx.bot.db.fetchrow(query, int(roleIDs[i]))
        rolesdata.append(result)
    return rolesdata

async def rolescheck_not_check(ctx, command):
    if ctx.author.id == 163691476788838401:
        return True
    else:
        rolesData = await getRolePerms(ctx)
        for role in rolesData:
            if role["administrator"] == True:
                return True
            elif role["muted"] == True:
                return False
            elif role[command] == True:
                return True
        return False

def pubquiz_active():
    async def predicate(ctx):
        query = "SELECT * FROM Guilds WHERE guildID = $1 AND ongoingpubquiz = true"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            return True
        else:
            return False
    return commands.check(predicate)

def pubquiz_not_active():
    async def predicate(ctx):
        query = "SELECT * FROM Guilds WHERE guildID = $1 AND ongoingpubquiz = false"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            return True
        else:
            return False
    return commands.check(predicate)