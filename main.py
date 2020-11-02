import discord, config
from discord.ext import commands
from db import cerate_user, update

bot = commands.Bot(command_prefix='/')


# class Memory():
#     keyy = None
#     value_particiant = None
#     fraction = None
#     role = None
#     type_of_armor = None
#     need_key = None
#     paid = None
#     frgn_user_id = None


@bot.command()
async def start(ctx):
	cerate_user(ctx.message.author.id, ctx.message.author.name)
	await ctx.send('Привет.\n\nСоздать заказ - /new_order\nПосмтореть историю закзов - /history')


@bot.command()
async def new_order(ctx, *, text):
	user_id = ctx.message.author.id
	value_particiant = ctx.kwargs['text'].split(' ')[0]
	keyy = ctx.kwargs['text'].split(' ')[1]
	update("keyy", keyy, user_id)
	update("value_particiant", value_particiant, user_id)
	update("step", 1, user_id)
	embedVar = discord.Embed(title="Создание заказа:", description=config.desc_1, color=000000)
	embedVar.add_field(name="Ключ:", value=keyy, inline=True)
	embedVar.add_field(name="Количество людей:", value=value_particiant, inline=True)
	message = await ctx.send(embed=embedVar)
	await message.add_reaction('1️⃣')
	await message.add_reaction('2️⃣')
	await message.add_reaction('3️⃣')
	await message.add_reaction('4️⃣')
	await message.add_reaction('5️⃣')
	await message.add_reaction('6️⃣')
	await message.add_reaction('7️⃣')
	await message.add_reaction('8️⃣')
	await message.add_reaction('9️⃣')
	await message.add_reaction('🔟')
	await message.add_reaction('#️⃣')
	await message.add_reaction('*️⃣')
	await message.add_reaction('❌')


@bot.event
async def on_raw_reaction_add(payload):
	channel = bot.get_channel(772361007615311876)
	user_id = payload.user_id
	emoji = payload.emoji.name
	if user_id != 772357764244570122:
		print("Польователь: {user_id} нажал на emoji: {emoji}".format(user_id=user_id, emoji=emoji))
		if emoji == '1️⃣':
			embedVar = discord.Embed(title="Создание заказа:", description=config.desc_2, color=000000)
			await channel.edit(embed=embedVar)
		else:
			pass


if __name__ == '__main__':
    bot.run(config.TOKEN)

