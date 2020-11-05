import discord, config, asyncio
from discord.ext import commands
from db import cerate_user, update, get_step, not_conf, get_order, get_other, get_cnt_role, active_orders, all_valid_orders

bot = commands.Bot(command_prefix='/')


@bot.command()
async def start(ctx):
	await ctx.send('Привет.\n\nСоздать заказ - /new_order [ключ] [кол-во участников]\nПосмтореть историю закзов - /order_history\nВыйти из заказа /cancel_order')


@bot.command()
async def cancel_order(ctx):
	user_id = int(ctx.message.author.id)
	update("step", 11, user_id)
	embedVar = discord.Embed(title="Заказ отменен", description='Создать новый заказ - /new_order [ключ] [кол-во участников]', color=000000)
	await ctx.send(embed=embedVar)


@bot.command()
async def panel(ctx):
	user_id = int(ctx.message.author.id)
	update("step", 11, user_id)
	orders = all_valid_orders(user_id)
	

@bot.command()
async def his(ctx):
	user_id = int(ctx.message.author.id)
	orders = all_valid_orders(user_id)
	print(orders)
	list_str = []
	for order in orders:
		step = order[10]
		if step == 9:
			status = 'working'
		elif step == 10:
			status = 'complete'
		raw_str = f'№{order[0]} - {order[4]} | STATUS: {status}'
		list_str.append(raw_str)
	finish_str = '\n'.join(list_str)
	embedVar = discord.Embed(title="История заказов", description=finish_str, color=000000)
	await ctx.send(embed=embedVar)


@bot.command()
async def new_order(ctx, key, people, *args):
	# print(args)
	cerate_user(int(ctx.message.author.id), str(ctx.message.author.name))
	user_id = int(ctx.message.author.id)
	update("keyy", str(key), int(user_id))
	update("value_particiant", str(people), int(user_id))
	cnt_role = get_cnt_role(user_id)
	cnt_user = int(get_other(user_id, 'value_particiant')[0][0])
	if args != ():
		nt = not_conf(user_id)
		fraction = args[0][1:]
		update('fraction', fraction, user_id)
		try: # Роль 1
			role1 = args[1][1:]
			role1_list = role1.split('-')
		except:
			role1 = None
		try: # Роль 2
			role2 = args[2][1:]
			role2_list = role2.split('-')
		except:
			role2 = None
		try: # Роль 3
			role3 = args[3][1:]
			role3_list = role3.split('-')
		except:
			role3 = None
		try: # Роль 4
			role4 = args[4][1:]
			role4_list = role4.split('-')
		except:
			role4 = None
		
		lists = [role1_list, role2_list, role3_list, role4_list]

		for l in lists:
			try:
				roles = eval(get_other(user_id, 'role')[0][0])
			except:
				roles = None
			try:
				armors = eval(get_other(user_id, 'type_of_armor')[0][0])
			except:
				armors = None
			try:
				nks = eval(get_other(user_id, 'need_key')[0][0])
			except:
				nks = None

			try:
				roles.append(l[0])
				update('role', f'{roles}', user_id)
				update("cnt_role", cnt_role[0][0]+1, user_id)
			except:
				pass
			try:
				armors.append(l[1])
				update('type_of_armor', f'{armors}', user_id)
			except:
				pass
			try:
				nks.append(l[2])
				update('need_key', f'{nks}', user_id)
			except:
				pass

		order = get_order(user_id)
		if cnt_role[0][0] == cnt_user:
			update("step", 8, user_id)
			embedVar = discord.Embed(title="Создание заказа:", description='Заказ создан в комнате №2', color=000000)
		elif cnt_role[0][0] != cnt_user:
			update("step", 3, user_id)
			embedVar = discord.Embed(title="Создание заказа:", description=config.desc_3, color=000000)
		embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
		embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
		embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
		embedVar.add_field(name="Фракция:", value=order['fraction'], inline=True)
		try:
			roles = eval(get_other(user_id, 'role')[0][0])
		except:
			roles = None
		try:
			armors = eval(get_other(user_id, 'type_of_armor')[0][0])
		except:
			armors = None
		try:
			nks = eval(get_other(user_id, 'need_key')[0][0])
		except:
			nks = None
		if roles == None:
			embedVar.add_field(name="Роли:", value='Не указано', inline=True)
		else:
			list_str = []
			for r, a, n in zip(roles, armors, nks):
				str_item = f'{r}-{a}(Нужен ключ: {n})'
				list_str.append(str_item)
			finish_str = '\n'.join(list_str)
		embedVar.add_field(name="Роли:", value=finish_str, inline=True)
		embedVar.add_field(name="Room:", value='2', inline=True)
		if cnt_role[0][0] == cnt_user:
			message = await ctx.send(embed=embedVar)
			await message.add_reaction('❌')
		elif cnt_role[0][0] != cnt_user:
			for emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '❌'):
				await message.add_reaction(emoji)
			
	else:
		nt = not_conf(user_id)
		update("step", 1, int(user_id))
		update("keyy", str(key), int(user_id))
		update("value_particiant", str(people), int(user_id))
		embedVar = discord.Embed(title="Создание заказа:", description=config.desc_2, color=000000)
		embedVar.add_field(name="Ключ:", value=str(key), inline=True)
		embedVar.add_field(name="Количество людей:", value=str(people), inline=True)
		message = await ctx.send(embed=embedVar)
		for emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '❌'):
			await message.add_reaction(emoji)


@bot.event
async def on_raw_reaction_add(payload):
	user_id = int(payload.user_id)
	# order = get_order(user_id)
	channel = bot.get_channel(773841835268767759)
	emoji = payload.emoji.name
	step = get_step(int(user_id))
	if user_id != 772357764244570122:
		if emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '#️⃣', '*️⃣', '❌') and step[0][0] == 2:
			update("step", 5, user_id)
			names = {"1️⃣": "Siege of Boralus", "2️⃣": "Freehold", "3️⃣": "Shrine of the Storm", "4️⃣": "Tol Dagor", 
				"5️⃣": "Waycrest Manor", "6️⃣": "Atal'Dazar", "7️⃣": "The MOTHERLODE!!!", "8️⃣": "Temple of Sethrailiss", 
				"9️⃣": "The Underrot", "🔟": "King's Rest", "#️⃣": "Junkyard", "*️⃣": "Workshop", "❌": "cancel"}
			if emoji == '❌':
				order = get_order(user_id)
				update("step", 4, user_id)
				embedVar = discord.Embed(title="Создание заказа:", description=config.desc_4, color=000000)
				embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
				embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
				embedVar.add_field(name="Фракция:", value=order['fraction'], inline=True)
				roles = eval(get_other(user_id, 'role')[0][0])
				nks = eval(get_other(user_id, 'need_key')[0][0])
				if roles == None:
					embedVar.add_field(name="Роли:", value='Не указано', inline=True)
				else:
					list_str = []
					for r, n in zip(roles, nks):
						str_item = f'{r}(Нужен ключ: {n})'
						list_str.append(str_item)
					finish_str = '\n'.join(list_str)
					embedVar.add_field(name="Роли:", value=finish_str, inline=True)
				message = await channel.send(embed=embedVar)
				for emoji in ('✅', '❌'):
					await message.add_reaction(emoji)

			else:
				for n in names:
					if emoji==n:
						update("key_name", names[n], user_id)
				order = get_order(user_id)
				pre_message = await channel.fetch_message(payload.message_id)
				await pre_message.delete()
				embedVar = discord.Embed(title="Создание заказа:", description=config.desc_5, color=000000)
				embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
				embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
				try:
					roles = eval(get_other(user_id, 'role')[0][0])
				except:
					roles = None
				try:
					armors = eval(get_other(user_id, 'type_of_armor')[0][0])
				except:
					armors = None
				try:
					nks = eval(get_other(user_id, 'need_key')[0][0])
				except:
					nks = None
				if roles == None:
					embedVar.add_field(name="Роли:", value='Не указано', inline=True)
				else:
					list_str = []
					for r, a, n in zip(roles, armors, nks):
						str_item = f'{r}-{a}(Нужен ключ: {n})'
						list_str.append(str_item)
					finish_str = '\n'.join(list_str)
					embedVar.add_field(name="Роли:", value=finish_str, inline=True)
				message = await channel.send(embed=embedVar)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '❌'):
						await message.add_reaction(emoji)
		
		elif emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '❌') and step[0][0] == 1:
			update("step", 3, user_id)
			names = {"1️⃣" : "EU-Horde", "2️⃣": "EU-Alliance", "3️⃣": "US-Horde", "4️⃣": "US-Alliance"}
			print(payload.message_id)
			pre_message = await channel.fetch_message(payload.message_id)
			await pre_message.delete()

			if emoji == '❌':
				order = get_order(user_id)
				update("step", 1, int(user_id))
				embedVar = discord.Embed(title="Создание заказа:", description=config.desc_1, color=000000)
				embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
				embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
				message = await channel.send(embed=embedVar)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '#️⃣', '*️⃣', '❌'):
					await message.add_reaction(emoji)
			else:
				cnt_role = get_cnt_role(user_id)
				cnt_user = int(get_other(user_id, 'value_particiant')[0][0])
				for n in names:
					if emoji==n:
						update("fraction", names[n], user_id)
				order = get_order(user_id)
				embedVar = discord.Embed(title="Создание заказа:", description=config.desc_3, color=000000)
				embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
				embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
				embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
				message = await channel.send(embed=embedVar)
				for emoji in ('➕', '✅', '❌'):
					await message.add_reaction(emoji)

		elif emoji in ('➕', '✅', '❌') and step[0][0] == 3:
			update("step", 4, user_id)
			pre_message = await channel.fetch_message(payload.message_id)
			await pre_message.delete()
			if emoji == '➕':
				order = get_order(user_id)
				embedVar = discord.Embed(title="Создание заказа:", description=config.desc_4, color=000000)
				embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
				embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
				if order['key_name']==None:
					pass
				else:
					embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
				embedVar.add_field(name="Фракция:", value=order['fraction'], inline=True)
				try:
					roles = eval(get_other(user_id, 'role')[0][0])
				except:
					roles = None
				try:
					armors = eval(get_other(user_id, 'type_of_armor')[0][0])
				except:
					armors = None
				try:
					nks = eval(get_other(user_id, 'need_key')[0][0])
				except:
					nks = None
				if roles == None:
					embedVar.add_field(name="Роли:", value='Не указано', inline=True)
				else:
					list_str = []
					for r, a, n in zip(roles, armors, nks):
						str_item = f'{r}-{a}(Нужен ключ: {n})'
						list_str.append(str_item)
					finish_str = '\n'.join(list_str)
					embedVar.add_field(name="Роли:", value=finish_str, inline=True)
				message = await channel.send(embed=embedVar)
				for emoji in ('✅', '❌'):
					await message.add_reaction(emoji)
			elif emoji == '✅':
				update("step", 9, user_id)
				order = active_orders(user_id)
				print(order)
				embedVar = discord.Embed(title="Создание заказа:", description='Заказ создан в комнате №2', color=000000)
				embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
				embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
				embedVar.add_field(name="Фракция:", value=order['fraction'], inline=True)
				try:
					roles = eval(order['role'])
				except:
					roles = None
				try:
					armors = eval(order['type_of_armor'])
				except:
					armors = None
				try:
					nks = eval(order['need_key'])
				except:
					nks = None
				if roles == None:
					embedVar.add_field(name="Роли:", value='Не указано', inline=True)
				else:
					list_str = []
					for r, a, n in zip(roles, armors, nks):
						str_item = f'{r}-{a}(Нужен ключ: {n})'
						list_str.append(str_item)
					finish_str = '\n'.join(list_str)
					embedVar.add_field(name="Роли:", value=finish_str, inline=True)
				embedVar.add_field(name="Room:", value='2', inline=True)
				message = await channel.send(embed=embedVar)
				await message.add_reaction('❌')
			elif emoji == '❌':
				update("step", 1, user_id)
				order = get_order(user_id)
				embedVar = discord.Embed(title="Создание заказа:", description=config.desc_2, color=000000)
				embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
				embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
				message = await channel.send(embed=embedVar)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '❌'):
					await message.add_reaction(emoji)
			
		elif emoji in ('✅', '❌') and step[0][0] == 4:
			cnt_role = get_cnt_role(user_id)
			update("cnt_role", cnt_role[0][0]+1, user_id)
			names = {"✅": "Да", "❌": "Нет"}
			need_key = get_other(user_id, 'need_key')
			for n in names:
				if emoji==n:
					if need_key[0][0] == None:
						list_nk = []
						list_nk.append(names[n])
						update("need_key", str(list_nk), user_id)
					else:
						clean_nk = eval(need_key[0][0])
						clean_nk.append(names[n])
						update("need_key", str(clean_nk), user_id)
			order = get_order(user_id)
			pre_message = await channel.fetch_message(payload.message_id)
			await pre_message.delete()
			if emoji == '✅':
				embedVar = discord.Embed(title="Создание заказа:", description=config.desc_1, color=000000)
			elif emoji == '❌':
				embedVar = discord.Embed(title="Создание заказа:", description=config.desc_5, color=000000)
			embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
			embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
			# embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
			embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
			try:
				roles = eval(get_other(user_id, 'role')[0][0])
			except:
				roles = None
			try:
				armors = eval(get_other(user_id, 'type_of_armor')[0][0])
			except:
				armors = None
			try:
				nks = eval(get_other(user_id, 'need_key')[0][0])
			except:
				nks = None
			if roles == None:
				embedVar.add_field(name="Роли:", value='Не указано', inline=True)
			else:
				list_str = []
				for r, a, n in zip(roles, armors, nks):
					str_item = f'{r}-{a}(Нужен ключ: {n})'
					list_str.append(str_item)
				finish_str = '\n'.join(list_str)
				embedVar.add_field(name="Роли:", value=finish_str, inline=True)
			message = await channel.send(embed=embedVar)
			if emoji == '✅':
				update("step", 2, user_id)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '#️⃣', '*️⃣', '❌'):
					await message.add_reaction(emoji)
			elif emoji == '❌':
				update("step", 5, user_id)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '❌'):
					await message.add_reaction(emoji)

		elif emoji in ('1️⃣', '2️⃣', '3️⃣', '❌') and step[0][0] == 5:
			update("step", 6, user_id)
			names = {"1️⃣" : "Tank", "2️⃣": "Dps", "3️⃣": "Heal", "❌": "cancel"}
			pre_message = await channel.fetch_message(payload.message_id)
			await pre_message.delete()

			if emoji == '❌':
				order = get_order(user_id)
				update("step", 4, user_id)
				embedVar = discord.Embed(title="Создание заказа:", description=config.desc_4, color=000000)
				message = await channel.send(embed=embedVar)
				embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
				embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
				embedVar.add_field(name="Фракция:", value=order['fraction'], inline=True)
				embedVar.add_field(name="Роли:", value='Не указано', inline=True)
				for emoji in ('✅', '❌'):
					await message.add_reaction(emoji)
			elif emoji == "1️⃣":
				need_key = get_other(user_id, 'role')
				for n in names:
					if emoji==n:
						if need_key[0][0] == None:
							list_nk = []
							list_nk.append(names[n])
							update("role", str(list_nk), user_id)
						else:
							clean_nk = eval(need_key[0][0])
							clean_nk.append(names[n])
							update("role", str(clean_nk), user_id)
				order = get_order(user_id)
				embedVar = discord.Embed(title="Создание заказа:", description=config.desc_6_tank, color=000000)
				embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
				embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
				embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
				roles = eval(get_other(user_id, 'role')[0][0])
				nks = eval(get_other(user_id, 'need_key')[0][0])
				if roles == None:
					embedVar.add_field(name="Роли:", value='Не указано', inline=True)
				else:
					list_str = []
					for r, n in zip(roles, nks):
						str_item = f'{r}(Нужен ключ: {n})'
						list_str.append(str_item)
					finish_str = '\n'.join(list_str)
					embedVar.add_field(name="Роли:", value=finish_str, inline=True)
				message = await channel.send(embed=embedVar)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '❌'):
					await message.add_reaction(emoji)
			else:
				need_key = get_other(user_id, 'role')
				for n in names:
					if emoji==n:
						if need_key[0][0] == None:
							list_nk = []
							list_nk.append(names[n])
							update("role", str(list_nk), user_id)
						else:
							clean_nk = eval(need_key[0][0])
							clean_nk.append(names[n])
							update("role", str(clean_nk), user_id)
				order = get_order(user_id)
				embedVar = discord.Embed(title="Создание заказа:", description=config.desc_6, color=000000)
				embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
				embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
				embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
				roles = eval(get_other(user_id, 'role')[0][0])
				nks = eval(get_other(user_id, 'need_key')[0][0])
				if roles == None:
					embedVar.add_field(name="Роли:", value='Не указано', inline=True)
				else:
					list_str = []
					for r, n in zip(roles, nks):
						str_item = f'{r}(Нужен ключ: {n})'
						list_str.append(str_item)
					finish_str = '\n'.join(list_str)
					embedVar.add_field(name="Роли:", value=finish_str, inline=True)
				message = await channel.send(embed=embedVar)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '❌'):
					await message.add_reaction(emoji)
		
		elif emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '❌') and step[0][0] == 6:
			update("step", 3, user_id)
			names = {"1️⃣" : "Латы", "2️⃣": "Кольчуга", "3️⃣": "Кожа", "4️⃣": "Ткань", "5️⃣": "Без брони", "❌": "cancel"}
			pre_message = await channel.fetch_message(payload.message_id)
			await pre_message.delete()

			if emoji == '❌':
				update("step", 5, user_id)
				order = get_order(user_id)
				embedVar = discord.Embed(title="Создание заказа:", description=config.desc_5, color=000000)
				embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
				embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
				embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
				embedVar.add_field(name="Роли", value='Не указано', inline=True)
				message = await channel.send(embed=embedVar)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '❌'):
					await message.add_reaction(emoji)
			else:
				need_key = get_other(user_id, 'type_of_armor')
				cnt_role = get_cnt_role(user_id)
				cnt_user = int(get_other(user_id, 'value_particiant')[0][0])
				print(cnt_role, cnt_user)
				for n in names:
					if emoji==n:
						if need_key[0][0] == None:
							list_nk = []
							list_nk.append(names[n])
							update("type_of_armor", str(list_nk), user_id)
						else:
							clean_nk = eval(need_key[0][0])
							clean_nk.append(names[n])
							update("type_of_armor", str(clean_nk), user_id)
				if cnt_role[0][0] != cnt_user:
					order = get_order(user_id)
					embedVar = discord.Embed(title="Создание заказа:", description=config.desc_3, color=000000)
					embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
					embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
					embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
					embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
					try:
						roles = eval(get_other(user_id, 'role')[0][0])
						armors = eval(get_other(user_id, 'type_of_armor')[0][0])
						nks = eval(get_other(user_id, 'need_key')[0][0])
					except:
						roles = None
						armors = None
						nks = None
					if roles == None:
						embedVar.add_field(name="Роли:", value='Не указано', inline=True)
					else:
						list_str = []
						for r, a, n in zip(roles, armors, nks):
							str_item = f'{r}-{a}(Нужен ключ: {n})'
							list_str.append(str_item)
						finish_str = '\n'.join(list_str)
					embedVar.add_field(name="Роли:", value=finish_str, inline=True)
					message = await channel.send(embed=embedVar)
					for emoji in ('➕', '✅'):
						await message.add_reaction(emoji)
				elif cnt_role[0][0] == cnt_user:
					update("step", 8, user_id)
					order = get_order(user_id)
					embedVar = discord.Embed(title="Создание заказа:", description='Заказ создан в комнате №2', color=000000)
					embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
					embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
					embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
					embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
					roles = eval(get_other(user_id, 'role')[0][0])
					armors = eval(get_other(user_id, 'type_of_armor')[0][0])
					nks = eval(get_other(user_id, 'need_key')[0][0])
					if roles == None:
						embedVar.add_field(name="Роли:", value='Не указано', inline=True)
					else:
						list_str = []
						for r, a, n in zip(roles, armors, nks):
							str_item = f'{r}-{a}(Нужен ключ: {n})'
							list_str.append(str_item)
						finish_str = '\n'.join(list_str)
						embedVar.add_field(name="Роли:", value=finish_str, inline=True)
					embedVar.add_field(name="Room:", value='2', inline=True)
					message = await channel.send(embed=embedVar)
					await message.add_reaction('❌')

		elif emoji == '✅' and step[0][0] == 7:
			update("step", 9, user_id)
			order = active_orders(user_id)
			embedVar = discord.Embed(title="Создание заказа:", description='Заказ создан в комнате №2', color=000000)
			embedVar.add_field(name="Ключ:", value=order['keyy'], inline=True)
			embedVar.add_field(name="Количество людей:", value=order['value_particiant'], inline=True)
			embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
			embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
			try:
				roles = eval(get_other(user_id, 'role')[0][0])
			except:
				roles = None
			try:
				armors = eval(get_other(user_id, 'type_of_armor')[0][0])
			except:
				armors = None
			try:
				nks = eval(get_other(user_id, 'need_key')[0][0])
			except:
				nks = None
			if roles == None:
				embedVar.add_field(name="Роли:", value='Не указано', inline=True)
			else:
				list_str = []
				for r, a, n in zip(roles, armors, nks):
					str_item = f'{r}-{a}(Нужен ключ: {n})'
					list_str.append(str_item)
				finish_str = '\n'.join(list_str)
				embedVar.add_field(name="Роли:", value=finish_str, inline=True)
			embedVar.add_field(name="Room:", value='2', inline=True)
			message = await channel.send(embed=embedVar)
			await message.add_reaction('❌')

		elif emoji == '❌' and step[0][0] == 8:
			update("step", 11, user_id)
			embedVar = discord.Embed(title="Заказ отменен", description='Создать новый заказ - /new_order [ключ] [кол-во участников]', color=000000)
			message = await channel.send(embed=embedVar)
		else:
			pass


if __name__ == '__main__':
    bot.run(config.TOKEN)

