import discord
from discord.ext import commands

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx):
        guild = ctx.guild
        author = ctx.author

        # prevent duplicate tickets (simple check)
        for channel in guild.channels:
            if channel.name == f"ticket-{author.name.lower()}":
                await ctx.send("You already have an open ticket.")
                return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{author.name}",
            overwrites=overwrites
        )

        await channel.send(
            f"{author.mention} 🎟️ Welcome to your ticket!\n"
            "A staff member will assist you soon.\n"
            "Type `!close` to close this ticket."
        )

        await ctx.send(f"Ticket created: {channel.mention}")

    @commands.command()
    async def close(self, ctx):
        if ctx.channel.name.startswith("ticket-"):
            await ctx.send("Closing ticket...")
            await ctx.channel.delete()
        else:
            await ctx.send("This is not a ticket channel.")

async def setup(bot):
    await bot.add_cog(Ticket(bot))
