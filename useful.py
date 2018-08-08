import discord, asyncio, sys, traceback, checks, useful, asyncpg, random
from discord.ext import commands
from types import FunctionType


def formatText(ctx, text):
    return text.replace("%user%", ctx.mention)

def formatTextLeave(ctx, text):
    return text.replace("%user%", ctx.display_name)

def getMenuEmoji(noOfOptions):
    #emojis = [["one", "1\u20e3"],["two", "2\u20e3"],["three", "3\u20e3"],["four", "4\u20e3"], ["five", "5\u20e3"],["six", "6\u20e3"], ["seven", "7\u20e3"],["eight", "8\u20e3"],["nine", "9\u20e3"],["ten", "\U0001f51f"]]
    emojis = ["0\u20e3", "1\u20e3", "2\u20e3", "3\u20e3", "4\u20e3", "5\u20e3", "6\u20e3", "7\u20e3", "8\u20e3", "9\u20e3", "\U0001f51f"]
    toReturn = []
    for i in range (0,noOfOptions):
        toReturn.append(emojis[i])
    toReturn.append("❌")
    return toReturn

async def menuFunction(ctx, titleText, options, footerText=None, timeoutTime = 60.0):
    descriptionText = "Options:"
    validAnswers = []
    for counter in range (0,len(options)):
        descriptionText+="\n"+str(options[counter][1][0])+": "+options[counter][0][0]
        validAnswers.append(options[counter][1])
    descriptionText += "\nx: Closes Menu"
    validAnswers.append(["x", "cancel", "exit"])
    embed = discord.Embed(title=titleText, description=descriptionText, colour=ctx.bot.getcolour())
    if footerText:
        embed.set_footer(text=footerText)
    menu = await ctx.channel.send(embed=embed)
    print(validAnswers)
    def confirmationcheck(msg):
        if ctx.channel.id == msg.channel.id and msg.author.id == ctx.author.id:
            for j in range(0,len(validAnswers)):
                if msg.content.lower() in validAnswers[j]:
                    return True
        return False
        ##return (msg.content.lower() in validAnswers) and ctx.channel.id == msg.channel.id and msg.author.id == ctx.author.id
    try:
        msg = await ctx.bot.wait_for('message', check=confirmationcheck, timeout=timeoutTime)
    except asyncio.TimeoutError:
        await menu.delete()
        await ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** - The menu has closed due to inactivity.")
    else:
        await menu.delete()
        if msg.content.lower() == "x" or msg.content.lower() == "cancel" or msg.content.lower() == "exit":
            exitmsg = await ctx.channel.send(":white_check_mark: | Exiting menu...")
            await asyncio.sleep(3)
            await exitmsg.delete()
        else:
            for k in range(0,len(options)):
                if msg.content.lower() in options[k][1]:
                    print(str(options[k][0][1]))
                    exec(str(options[k][0][1]))

            print("This should probably never be seen.")
        print("This should probably never be seen number 2.")

