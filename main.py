import discord
import requests
import json
from replit import db
import time
from keep_alive import keep_alive

# Create Intents object and set desired intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Initialize users and their money as a dictionary
if "users" not in db.keys():
  users_list = ['Aryan', 'Boris', 'Enzo', 'Florian', 'James', 'Jeremy', 'Tom', 'Ugo']
  db["users"] = {user: 0.0 for user in users_list}
else:
  db["users"] = dict(db["users"])

def update_user_money(name, new_money):
    users = dict(db["users"])
    users[name] = new_money
    db["users"] = users

def get_user_money(name):
    users = dict(db["users"])
    return users.get(name, None)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
      return

    if message.content.startswith("!help"):
        await message.channel.send(
            "Here are the available commands:\n"
            "**!help**: Displays this help message.\n"
            "**!list**: Lists all users and their money.\n"
            "**!check <name>**: Checks the money for a user.\n\n"
            "Only Devs :\n"
            "**!add <name> <amount>**: Adds money to a user.\n"
            "**!rm <name> <amount>**: Removes money from a user.\n"
            "**!set <name> <amount>**: Sets the money for a user.\n"
            "**!exit**: Disables the bot.")
        return

        

      
    if message.content.startswith("!list"):
      users = dict(db["users"])  # Explicitly convert to dictionary
      response = "\n".join(f"{user}: {money}€" for user, money in users.items())
      await message.channel.send(f"Current users and their money:\n{response}")

    if message.content.startswith("!check"):
      try:
          name = message.content.split("!check ", 1)[1]
          money = get_user_money(name)
          if money is not None:
              await message.channel.send(f"{name} has {money}€.")
          else:
              await message.channel.send(f"{name} is not in the database.")
      except IndexError:
          await message.channel.send("Usage: !check <name>")

    if message.content.startswith("!add") or message.content.startswith("!set") or message.content.startswith("!rm") or message.content.startswith("!exit"):
      role = discord.utils.get(message.author.guild.roles, name="Developpeur")
      if role not in message.author.roles:
          await message.channel.send("You don't have the Developpeur role.")
          time.sleep(1.5)
          await message.channel.send("No role, no perms.")
          time.sleep(2)
          await message.channel.send("https://tenor.com/view/noperms-gif-27260516")
          return
    if message.content.startswith("!add"):
        try:
            _, name, amount = message.content.split(" ")
            amount = float(amount)
            if name in db["users"]:
                db["users"][name] += amount
                await message.channel.send(f"Added {amount}€ to {name}. New balance: {db['users'][name]}€.")
            else:
                await message.channel.send(f"{name} is not in the database.")
        except ValueError:
            await message.channel.send("Usage: !add <name> <amount>")
        except IndexError:
            await message.channel.send("Usage: !add <name> <amount>")

    if message.content.startswith("!rm"):
        try:
            _, name, amount = message.content.split(" ")
            amount = float(amount)
            if name in db["users"]:
                db["users"][name] -= amount
                await message.channel.send(f"Removed {amount}€ from {name}. New balance: {db['users'][name]}€.")
            else:
                await message.channel.send(f"{name} is not in the database.")
        except ValueError:
            await message.channel.send("Usage: !rm <name> <amount>")
        except IndexError:
            await message.channel.send("Usage: !rm <name> <amount>")

    if message.content.startswith("!set"):
        try:
            _, name, amount = message.content.split(" ")
            amount = float(amount)
            update_user_money(name, amount)
            await message.channel.send(f"Set {name}'s balance to {amount}€.")
        except ValueError:
            await message.channel.send("Usage: !set <name> <amount>")
        except IndexError:
            await message.channel.send("Usage: !set <name> <amount>")
    if message.content.startswith("!exit"):
      await message.channel.send("Disabling the Bot")
      exit(0)

client.run("MTMyNzE4NTMzMTE1MzQwODAwMA.G6XvnL.h5EtCsH-4Vuy9BVXfKBd66KqreLj919dMXBXpw")
