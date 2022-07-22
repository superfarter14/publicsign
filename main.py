from typing import final
import discord
from discord.ext import commands
coachRoles = commands.has_any_role('Franchise Owner', 'Head Coach', 'General Manager')
teams = ["Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills", "Carolina Panthers",
             "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns", "Dallas Cowboys", "Denver Broncos",
             "Detroit Lions", "Green Bay Packers", "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars",
             "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams",
             "Miami Dolphins",
             "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants", "New York Jets",
             "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers", "Seattle Seahawks",
             "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"]


bot = commands.Bot(command_prefix=',', debug_guilds=[999368523451215882], intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('online \n ---------------')
    

@bot.slash_command(description='force signs a member')
@coachRoles
async def sign(ctx, member: discord.Member):

    au = [role for role in ctx.author.roles]
    mem = [role for role in member.roles]

    for roles in mem:
        if roles.name in teams:
            await ctx.respond(f"that player is already in a team! \n > Team : `{roles.name}`", ephemeral=True)
            return


    for roles in au:
        if roles.name in teams:
            team = discord.utils.get(ctx.guild.roles, name=roles.name)

            try:
                await member.add_roles(team)
                free = discord.utils.get(ctx.guild.roles, name="Free Agent")
                await member.remove_roles(free)
            except:
                await ctx.respond("error giving role", ephemeral=True)
                return
            finally:

                
                e = discord.Embed(title="New signing!", description=f" > **A Team has signed a member.** \n > **Team** : {team.mention} \n > **Coach** : {ctx.author.mention} \n > **Roster limit** : `{len(team.members)}`", color=team.color)
                e.add_field(name="Player", value=f"{member.mention} `{member}`")
                
                await ctx.respond("signed member", ephemeral=True)
                await ctx.channel.send(embed=e)
                return

@bot.slash_command(description='force signs a member')
@coachRoles
async def release(ctx, member: discord.Member):
    au = [role for role in ctx.author.roles]
    mem = [role for role in member.roles]

    for roles in au:
        if roles.name in teams:
            global teamError
            teamError = roles.name

    for roles in mem:
        if roles.name in teams:
            if roles.name is not teamError:
                await ctx.respond(f"that player isnt in your team! \n > Team : `{roles.name}`", ephemeral=True)
                return
            else:
                pass

    try:
        team = discord.utils.get(ctx.guild.roles, name=teamError)
        free = discord.utils.get(ctx.guild.roles, name="Free Agent")
        await member.add_roles(free) 
        await member.remove_roles(team)
    except:
        await ctx.respond('error', ephemeral=True)
        return
    finally:
        e = discord.Embed(title="A new release!", description=f" > **A Team has released a member.** \n > **Team** : {team.mention} \n > **Coach** : {ctx.author.mention} \n > **Roster limit** : `{len(team.members)}`", color=team.color)
        e.add_field(name="Player", value=f"{member.mention} `{member}`")

        await ctx.respond("released member", ephemeral=True)
        await ctx.channel.send(embed=e)
        return

bot.run('bot_token')
