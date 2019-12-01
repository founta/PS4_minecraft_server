import discord
import commands as command

import asyncio

user_file_name = "users.txt"
vital_name = "vital.txt"

user_file = open(user_file_name, "r")
all_ids = user_file.readlines()
user_file.close()

psn_discord_ids = dict()

command_by = []

for id in all_ids:
    id = id.strip()
    if id is not "":
        two_id = id.split('\t')
        psn_discord_ids[two_id[1]] = two_id[0]

print(psn_discord_ids)

vital = open(vital_name, "r")
vital_info = vital.readlines()
token = vital_info[0].strip()
channel = discord.Object(id = vital_info[1])
vital.close()

client = discord.Client()


@client.event
async def on_ready():
    await command.init_controller()
    print("controller on")
    await client.send_message(channel, "Standing by...")

@client.event
async def on_message(message):
    
    #don't pay the bot's messages any mind
    if (message.author == client.user):
        return

    #parse message and carry out commands
    lines = message.content.split()
    if lines[0].lower() == "register": #associate a discord id with a PSN id
        if len(lines) is not 2 :
            await client.send_message(message.author, "Failure!\nregister command usage:\nregister your_psn_id")
            return
        psn = lines[1].strip()
        disc = str(message.author.id)
        print("register\t" + psn + "\t" + disc)
        if disc in psn_discord_ids : #cant register a new psn if you've already registered an id
            if psn_discord_ids[disc] == psn:
                await client.send_message(message.author, "You've already registered this discord id as the PSN id '" + psn_discord_ids[disc])
            else:
                await client.send_message(message.author, "Failure!\nYour discord id is registered as the PSN id '" + psn_discord_ids[disc] + "'\nContact your nearest admin to remove this binding, if need be")
            return
        for disc_id, psn_id in psn_discord_ids.items():
            if psn_id == psn:
                await client.send_message(message.author, "Failure!\nThe PSN id '"+psn+"' is already registered to a discord account.\nContact your nearest admin if you suspect skullduggery\n")
                return
        psn_discord_ids[disc] = psn
        with open(user_file_name, "a") as file:
            file.write(psn + "\t" + disc + "\n")
        await client.send_message(message.author, "Success! {0} (Discord user id {1}) registered as PSN '{2}'".format(message.author.name, message.author.id, psn))
    elif lines[0].lower() == "invite":
        if str(message.author.id) not in psn_discord_ids:
            await client.send_message(message.author, "Failure!\nYou are not yet registered with a PSN id.\nPlease send \"register your_PSN_id\". With your actual PSN id, of course.")
            return
        else:
            await command.open_invite_screen()
            await command.search()
            await command.write_kb_str(psn_discord_ids[str(message.author.id)])
            await command.select_player()
            await command.send_invite()
            await command.close_invite_screen()
            await command.close_invite_screen()
            print ("invite "+psn_discord_ids[str(message.author.id)]);
            await client.send_message(message.author, "Invite sent to "+psn_discord_ids[str(message.author.id)])


client.run(token)
    