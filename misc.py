import discord, asyncio, sys, traceback, checks, inflect, useful, random
from discord.ext import commands

class miscCog:
    def __init__(self, bot):
        self.bot = bot
        self.deleteBlueText = False

    def blueTextFunction(self, userText, spaces):
        blueText = ""
        for counter in range(0,len(userText)):
            if userText[counter].isalpha() and spaces == True:
                blueText += ":regional_indicator_" + userText[counter].lower() + ": "
            elif userText[counter].isalpha() and spaces == False:
                blueText += ":regional_indicator_" + userText[counter].lower() + ":"
            elif userText[counter].isdigit():
                blueText += ":" + inflect.engine().number_to_words(userText[counter]) + ":"
            else:
                blueText += userText[counter]
        return blueText

    @commands.command(name="bluetext", aliases=['bt'])
    @checks.is_not_banned()
    async def bluetext(self, ctx, *, userText):
        toOutput = self.blueTextFunction(userText, False)
        await ctx.channel.send(toOutput)
        if self.deleteBlueText:
            await ctx.message.delete()

    @commands.command(name="bluetextcode", aliases=['bluetextmarkup', 'btc', 'btmu'])
    @checks.is_not_banned()
    async def bluetextcode(self, ctx, *, userText):
        toOutput = self.blueTextFunction(userText, True)
        await ctx.channel.send(":white_check_mark | **"+ctx.author.display_name+"** here's your code:")
        await ctx.channel.send("```" + toOutput + "```")
        if self.deleteBlueText and ctx.author.id == 163691476788838401:
            await ctx.message.delete()

    @commands.command()
    @checks.is_not_banned()
    async def cute(self, ctx, member):
        memberID = useful.getid(member)
        try:
            toOutput = self.blueTextFunction((ctx.guild.get_member(memberID).nick +" is cute and valid and i love them"), False)
        except TypeError:
            toOutput = self.blueTextFunction((ctx.guild.get_member(memberID).name +" is cute and valid and i love them"), False)
        await ctx.channel.send(toOutput + ":heartpulse:")
        if self.deleteBlueText and ctx.author.id == 163691476788838401:
            await ctx.message.delete()

    @commands.command(name="togglebluetextdelete", aliases=['deletebluetext', 'tbtd'], hidden = True)
    @checks.justme()
    async def toggleBlueTextDelete(self, ctx):
        self.deleteBlueText = not self.deleteBlueText
        if self.deleteBlueText:
            await ctx.channel.send(":white_check_mark: | Hiding bluetext commands!")
        else:
            await ctx.channel.send(":white_check_mark: | No longer hiding bluetext commands!")

    @commands.command(name="conch", aliases=['shell'])
    @checks.is_not_banned()
    async def conch(self, ctx):
        randomNumber = random.randint(0,19)
        conchName = ("**" +ctx.author.name + "** | The conch says:")
        conchValue = ('"'+self.bot.outcomes[randomNumber]+ '."')
        embed = discord.Embed(colour=self.bot.conchcolour(randomNumber))
        embed.add_field(name=conchName, value = conchValue)
        embed.set_image(url="https://media1.tenor.com/images/0181e2d7787313c7de0b8acab72dde7f/tenor.gif?itemid=3541653")
        embed.set_footer(text="THE SHELL HAS SPOKEN")
        await ctx.channel.send(embed = embed)

    @commands.command(name="eightball", aliases=['8ball'])
    @checks.is_not_banned()
    async def eightball(self, ctx):
        randomNumber = random.randint(0, 19)
        eightballName = ("**" + ctx.author.name + "** - The 8ball says:")
        eightballValue = ('"' + self.bot.outcomes[randomNumber] + '."')
        await ctx.channel.send(":8ball: | "+eightballName + " " + eightballValue)

    @commands.command(name="roll")
    @checks.is_not_banned()
    async def roll(self, ctx, diceCommand):
        diceCommand = diceCommand.lower()
        diceCommand = diceCommand.split("d")
        if len(diceCommand) != 2:
            await ctx.channel.send(":no_entry: | Incorrect command usage. Correct usage is `traa!roll 1d20`")
        else:
            succeeded = 1
            try:
                repeats = int(diceCommand[0])
            except:
                await ctx.channel.send(":no_entry: | Incorrect command usage. Correct usage is `traa!roll 1d20`")
                succeeded = 0
            try:
                throws = int(diceCommand[1])
            except:
                await ctx.channel.send(":no_entry: | Incorrect command usage. Correct usage is `traa!roll 1d20`")
                succeeded = 0
            if succeeded == 1:
                if throws > 0 and throws < 100001 and repeats > 0 and repeats < 101:
                    total = 0
                    toOutput = []
                    for counter in range (0,repeats):
                        rollresult = random.randint(1,throws)
                        total = total + rollresult
                        toOutput.append(str(rollresult))
                    toOutput = ', '.join(toOutput)
                    await ctx.channel.send(":game_die: | Rolling a **"+str(throws)+"** sided die **" + str(repeats)+" **time(s) ... **"+ctx.author.display_name+"** rolled: **" + str(toOutput) + "** for a total of: **" +str(total)+"**.")
                elif throws > 0 and throws < 100001:
                    await ctx.channel.send(":no_entry: | You can only throw between 1 and 100 dice at a time.")
                elif repeats > 0 and repeats < 101:
                    await ctx.channel.send(":no_entry: | You can only throw dice with between 1 and 100000 sides.")
                else:
                    await ctx.channel.send(":no_entry: | Incorrect command usage. Correct usage is `traa!roll 1d20`")

    @commands.command(name="choose", alises=['choice'])
    @checks.is_not_banned()
    async def choose(self, ctx, *, choices):
        choices = choices.split(" | ")
        if len(choices) < 2 or (len(choices)==2 and choices[0] == choices[1]):
            await ctx.channel.send(":no_entry: | Please enter at least two choices separated with ` | `!")
        else:
            choice = random.randint(0,len(choices)-1)
            await ctx.channel.send(":white_check_mark: | **"+ctx.author.display_name+"** I choose **"+choices[choice]+" **.")

    @commands.command(name='flip', alises=['coin', 'coinflip'])
    @checks.is_not_banned()
    async def flip(self, ctx):
        result = random.randint(0,1)
        if result == 1:
            await ctx.channel.send(":cd: | **"+ctx.message.author.display_name+"** flipped a coin and got: **heads!**")
        else:
            await ctx.channel.send(":dvd: | **"+ctx.message.author.display_name+"** flipped a coin and got: **tails!**")

def setup(bot):
    bot.add_cog(miscCog(bot))