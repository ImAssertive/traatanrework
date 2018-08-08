import discord, asyncio, sys, traceback, checks, useful, asyncpg, random
from discord.ext import commands

async def update(ctx, updateTable, updateLocation, updateValue, whereLocation, whereValue):
    updateTable = cleantext(updateTable)
    updateLocation = cleantext(updateLocation)
    whereLocation = cleantext(whereLocation)
    connection = await ctx.bot.db.acquire()
    async with connection.transaction():
        query = "UPDATE "+updateLocation+" SET banned = $1 WHERE "+whereLocation+" = $2"
        await ctx.bot.db.execute(query, updateValue, whereValue)
    await ctx.bot.db.release(connection)

def cleantext(uncleanText):
    cleanedText = ""
    for counter in range(0, len(uncleanText)):
        if uncleanText[counter].isalpha() or uncleanText[counter].isdigit():
            cleanedtext += text[counter]
    print(cleanedText)
    return cleanedText
