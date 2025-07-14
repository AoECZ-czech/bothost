import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")

@bot.tree.command(name="ping", description="Replies with Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

@bot.tree.command(name="kick", description="Kick a member from the server (Admins only)")
@app_commands.describe(member="The member to kick")
async def kick(interaction: discord.Interaction, member: discord.Member):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You must be an admin to use this command.", ephemeral=True)
        return

    try:
        await member.kick(reason=f"Kicked by {interaction.user}")
        await interaction.response.send_message(f"✅ {member} has been kicked.")
    except Exception as e:
        await interaction.response.send_message(f"❌ Failed to kick {member}. Error: {e}", ephemeral=True)

keep_alive()
bot.run(os.environ['TOKEN'])
