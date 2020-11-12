import discord, config, asyncio, system, math
from discord.ext import commands
from db import history_customer, history_executor, ended, update8, update9, not_conf, active_orders_customer, active_orders_executor, get_order_id, get_order, get_executor, get_customer, update, cerate_executor, create_order, cerate_customer

bot = commands.Bot(command_prefix='/')


@bot.command()
async def start(ctx):
	await ctx.send('Привет.\n\nСоздать заказ - /new_order [ключ] [кол-во участников]\nПосмтореть историю закзов - /order_history\nВыйти из заказа /cancel_order')


@bot.command()
async def cancel_order(ctx):
	if int(ctx.channel.id) != 774270476305563679:
		user_id = int(ctx.message.author.id)
		update("orders", "step", 11, user_id)
		embedVar = discord.Embed(title="Заказ отменен", description='Создать новый заказ - /new_order [ключ] [кол-во участников]', color=000000)
		await ctx.send(embed=embedVar)


@bot.command()
async def end(ctx, order_id):
	if int(ctx.channel.id) != 774270476305563679:
		try:
			ended("orders", "step", 12, int(order_id), int(ctx.message.author.id))
			await ctx.send(f"Заказ №{order_id} закрыт.")
		except:
			await ctx.send("Для тебя эта команда не доступна")


@bot.command()
async def not_accept(ctx, order_id, *, text):
	if int(ctx.channel.id) != 774270476305563679:
		order = get_order_id(order_id)
		executors_id = eval(order['executors_id'])
		for executor in executors_id:
			member = bot.get_user(executor)
			await member.send(f"Твой заказ №{order_id} не приняли.\nПричина: {text}")


@bot.command()
async def create(ctx):
	channel = bot.get_channel(776341478539657267)
	room = await channel.create_text_channel(f'M1')
	invitelinknew = await channel.create_invite(destination = int(room.id), xkcd = True, max_uses = 1)
	embed=discord.Embed(title="Discord Invite Link", description=invitelinknew, color=000000)
	await ctx.send(embed=embed)


@bot.command()
async def history(ctx):
	if int(ctx.channel.id) != 774270476305563679:
		history_orders = history_executor(int(ctx.message.author.id))
		embedVar = discord.Embed(title="История заказов:", description=history_orders, color=000000)
		await ctx.send(embed=embedVar)


@bot.command()
async def cab(ctx):
	if int(ctx.channel.id) != 774270476305563679:
		cerate_executor(int(ctx.message.author.id), str(ctx.message.author.name))
		executor = get_executor(int(ctx.message.author.id))
		active_orders = active_orders_executor(int(ctx.message.author.id))
		embedVar = discord.Embed(title="Личный кабинет:", description=f"Активные заказы: {active_orders}\n\n\
																		Команды для управления заказом:\n\
																		/prof [id заказа] [link] - отправить отчет проделанной работы\n\
																		/msg [id заказа] - отправить сообщение заказчику\n\n\
																		Пример: /prof 91 https://i.imgur.com/S2NmPv2.jpegn\n\
																		(Ссылка на изображение доказательства)", color=000000)
		embedVar.add_field(name="Баланс:", value=executor['balance'], inline=True)
		embedVar.add_field(name="Кошелек для выплат:", value=f"Платежная система: {executor['wallet_name']}\nНомер кошелька: {executor['wallet_address']}", inline=True)
		embedVar.add_field(name="Команды:", value=config.commands_cab, inline=True)
		await ctx.send(embed=embedVar)


@bot.command()
async def prof(ctx, order_id, link):
	if int(ctx.channel.id) != 774270476305563679:
		channel = bot.get_channel(773841835268767759)
		order = get_order_id(order_id)
		user_id = int(ctx.message.author.id)
		if user_id in eval(order['executors_id']):
			member = bot.get_user(order['customer_id'])
			await member.send(f"Заказ №{order_id} выполнен.\nФото-доказательство: {link}")
		else:
			await member.ctx(f"Ты ошибся заказом(")


@bot.command()
async def choose(ctx, wallet_name, wallet_address):
	if int(ctx.channel.id) != 774270476305563679:
		update('executors', 'wallet_name', str(wallet_name), int(ctx.message.author.id))
		update('executors', 'wallet_address', str(wallet_address), int(ctx.message.author.id))
		await ctx.send(f"Кошелёк изменен: {wallet_name} - {wallet_address}")


@bot.command()
async def msg(ctx, order_id, *, text):
	if int(ctx.channel.id) != 774270476305563679:
		order = get_order_id(order_id)
		user_id = int(ctx.message.author.id)
		if user_id in eval(order['executors_id']): 
			member = bot.get_user(user_id)
			await channel.send(f"Сообщение от {ctx.message.author.name} по заказу №{order_id}\n\n{text}")
		else:
			await member.ctx(f"Ты ошибся заказом(")


@bot.command()
async def panel(ctx):
	if int(ctx.channel.id) != 774270476305563679:
		cerate_customer(int(ctx.message.author.id), str(ctx.message.author.name))
		orders = active_orders_customer(int(ctx.message.author.id))
		embedVar = discord.Embed(title="Меню заказчика", description=config.user_panel1, color=000000)
		embedVar.add_field(name="Текущие заказы:", value=orders, inline=True)
		embedVar.add_field(name="Команды:", value=config.commands, inline=True)
		await ctx.send(embed=embedVar)


@bot.command()
async def close(ctx, order_id):
	if int(ctx.channel.id) != 774270476305563679:
		order = get_order_id(order_id)
		user_id = int(ctx.message.author.id)
		if user_id == order['customer_id'] and order['step'] not in (9, 10, 12, 13):
			update("orders", "step", 11, int(order_id))
			await ctx.send(f"Заказ №{order_id} закрыт.")
		else:
			await ctx.send(f"Заказ №{order_id} нельзя закрыть.")
		

@bot.command()
async def his(ctx):
	if int(ctx.channel.id) != 774270476305563679:
		history = history_customer("customer_id", int(ctx.message.author.id))
		embedVar = discord.Embed(title="История заказов", description=history, color=000000)
		await ctx.send(embed=embedVar)


@bot.command()
async def comment(ctx, *, text):
	if int(ctx.channel.id) != 774270476305563679:
		order = get_order(int(ctx.message.author.id))
		if order['step'] == 8:
			try:
				channel_orders = bot.get_channel(774270476305563679)
				update9("link", text, int(ctx.message.author.id))
				order2 = get_order(int(ctx.message.author.id))
				update9("step", 3, int(ctx.message.author.id))
				list_roles = system.return_roles(int(ctx.message.author.id))
				embedVar = discord.Embed(title="Создание заказа:", description='Заказ создан в комнате №2', color=000000)
				embedVar.add_field(name="Ключ:", value=order2['lvl_key'], inline=True)
				embedVar.add_field(name="Цена:", value=str(order2['price'])+'₽', inline=True)
				embedVar.add_field(name="Количество людей:", value=order2['cnt_executors'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order2['key_name'], inline=True)
				embedVar.add_field(name="Фракция:", value=order2['fraction'], inline=True)
				embedVar_order = discord.Embed(title="Новый заказ:", description=f"№{order2['id']} - {order2['key_name']}", color=000000)
				embedVar_order.add_field(name="Количество людей:", value=order2['cnt_executors'], inline=True)
				embedVar_order.add_field(name="Ключ:", value=order2['lvl_key'], inline=True)
				embedVar_order.add_field(name="Фракция:", value=order2['fraction'], inline=True)
				embedVar.add_field(name="Роли:", value=list_roles, inline=True)
				embedVar_order.add_field(name="Роли:", value=list_roles, inline=False)
				embedVar.add_field(name="Комментарий:", value=order2['link'], inline=True)
				embedVar.add_field(name="Цена:", value=order2['price'], inline=True)
				embedVar.add_field(name="Room:", value='#заказы', inline=True)
				message = await ctx.send(embed=embedVar)
				embedVar_order.add_field(name="Комментарий:", value=order2['link'], inline=True)
				embedVar_order.add_field(name="Цена:", value=str(order2['price'])+'₽', inline=True)
				embedVar_order.add_field(name="Действия:", value="✅ - откликнуться", inline=True)
				msg = await channel_orders.send(f"Заказ №{order2['id']}", embed=embedVar_order)
				update9("step", 9, int(ctx.message.author.id))
				await msg.add_reaction('✅')
			except:
				await ctx.send('Эта команда не доступна')
		else:
			await ctx.send('Комментарий можно оставить позже')


@bot.command()
async def new_order(ctx, key=None, people=None, *args):
	if int(ctx.channel.id) != 774270476305563679:
		channel_orders = bot.get_channel(774270476305563679)
		cerate_customer(int(ctx.message.author.id), str(ctx.message.author.name))
		user_id = int(ctx.message.author.id)
		not_conf(user_id)
		create_order(user_id, str(key), int(people))
		order = get_order(user_id)
		price_dict = {10: 40, 11: 40, 12: 60, 13: 60, 14: 80, 15: 80, 16: 100, 17: 120, 18: 160, 19: 200, 20: 240}
		try:
			list_key = key.split('x')
			keyy = int(list_key[0])
			cnt_keyy = int(list_key[1])
			price = price_dict[keyy] * cnt_keyy
			comission = math.ceil((float(price * 12 / 100)/10)*10)
		except:
			price = price_dict[int(key)]
			comission = math.ceil((float(price * 12 / 100)/10)*10)
		update9("price", price+comission, user_id)
		update9("comission", comission, user_id)
		update("customers", "credit", float(price+comission), user_id)

		if key != None and people != None:
			update9("lvl_key", str(key), user_id)
			update9("cnt_executors", int(people), user_id)
			cnt_executors = order['cnt_executors']
			list_roles = []
			link = "Ссылка на персонажа не указана"
			for arg in args:
				if arg[:1] == '@':
					integ = system.return_digits(arg)
					if integ == []:
						list_roles.append(arg[1:])
					elif integ != []:
						for i in range(0, integ[0]):
							cnt_symbols = len(str(i))+1
							list_roles.append(arg[1:-cnt_symbols])
				else:
					link = arg

			if len(list_roles) > 1:
				if (len(list_roles)-1) == int(people):
					update9("step", 8, user_id)
					embedVar = discord.Embed(title="Создание заказа:", description='Заказ создан в комнате #заказы', color=000000)
					embedVar.add_field(name="Ключ:", value=key, inline=True)
					embedVar.add_field(name="Количество людей:", value=people, inline=True)
					embedVar.add_field(name="Фракция:", value=list_roles[0], inline=True)
					embedVar.add_field(name="Роли:", value='\n'.join(list_roles[1:]), inline=False)
					embedVar.add_field(name="Комментарий:", value=link, inline=True)
					embedVar.add_field(name="Цена:", value=str(price+comission)+'₽', inline=True)
					embedVar.add_field(name="Room:", value='#заказы', inline=True)
					message = await ctx.send(embed=embedVar)
					# await message.add_reaction('❌')

					embedVar_order = discord.Embed(title="Новый заказ:", description=f"№{order['id']}", color=000000)
					embedVar_order.add_field(name="Ключ:", value=key, inline=True)
					embedVar_order.add_field(name="Количество людей:", value=cnt_executors, inline=True)
					embedVar_order.add_field(name="Фракция:", value=list_roles[0], inline=True)
					embedVar_order.add_field(name="Роли:", value='\n'.join(list_roles[1:]), inline=False)
					embedVar_order.add_field(name="Ссылка:", value=link, inline=True)
					embedVar_order.add_field(name="Цена:", value=str(price+comission)+'₽', inline=True)
					embedVar_order.add_field(name="Дейсвия:", value="✅ - откликнуться", inline=True)
					msg = await channel_orders.send(f"Заказ №{order['id']}", embed=embedVar_order)
					await msg.add_reaction('✅')
					roles = {}
					for r in list_roles[1:]:
						role = {}
						list_role = r.split('-')
						role['role'] = list_role[0]
						role['armor'] = list_role[1]
						try:
							role['key'] = list_role[2]
						except:
							role['key'] = 'Без ключа'
						roles[str(list_roles[1:].index(r)+1)] = role
					update9("roles", str(roles), user_id)
					update9("step", 9, user_id)
				else:
					await ctx.send("Число участников не совпадает с количеством ролей")
			else:
				embedVar = discord.Embed(title=f"Создание заказа №{order['id']}:", description=config.desc_2, color=000000)
				embedVar.add_field(name="Ключ:", value=key, inline=True)
				embedVar.add_field(name="Цена:", value=str(price+comission)+'₽', inline=True)
				embedVar.add_field(name="Количество людей:", value=people, inline=True)
				msg = await ctx.send(embed=embedVar)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '❌'):
					await msg.add_reaction(emoji)
				update9("step", 1, user_id)
		else:
			await ctx.send("Указаны не все данные.\nПример: /new_order 12 4\n(/new_order [ключ] [количество участников])")


@bot.event
async def on_raw_reaction_add(payload):
	user_id = int(payload.user_id)
	user_name = bot.get_user(user_id)
	channel_orders = bot.get_channel(774270476305563679)
	emoji = payload.emoji.name
	if user_id != 772357764244570122:
		step_order = get_order(user_id)
		try:
			step = step_order['step']
		except:
			step = 9
		member = bot.get_user(user_id)
		if emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '#️⃣', '*️⃣') and step == 2:
			update9("step", 5, user_id)
			names = config.keyses

			order = get_order(user_id)
			for n in names:
				if emoji==n:
					if order['roles'] == None:
						dict_role = {}
						role = {}
						role['key'] = names[n]
						dict_role['0'] = role
						update9("roles", str(dict_role), user_id)
						update9("key_name", str(names[n]), user_id)
					else:
						dict_role = eval(order['roles'])
						role = {}
						role['key'] = 'Без ключа'
						dict_role['0'] = role
						update9("roles", str(dict_role), user_id)
						update9("key_name", str(names[n]), user_id)
			pre_message = await member.fetch_message(payload.message_id)
			await pre_message.delete()
			order2 = get_order(user_id)
			list_roles = system.return_roles(user_id)
			embedVar = discord.Embed(title=f"Создание заказа №{order2['id']}:", description=config.desc_5, color=000000)
			embedVar.add_field(name="Ключ:", value=order2['lvl_key'], inline=True)
			embedVar.add_field(name="Цена:", value=str(order2['price'])+'₽', inline=True)
			embedVar.add_field(name="Количество людей:", value=order2['cnt_executors'], inline=True)
			embedVar.add_field(name="Название ключа:", value=order2['key_name'], inline=True)
			embedVar.add_field(name="Роли:", value=list_roles, inline=True)
			message = await member.send(embed=embedVar)
			for emoji in ('1️⃣', '2️⃣', '3️⃣', '❌'):
					await message.add_reaction(emoji)
		
		elif emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣') and step == 1:
			update9("step", 3, user_id)
			names = config.fractions
			pre_message = await member.fetch_message(payload.message_id)
			await pre_message.delete()

			for n in names:
				if emoji==n:
					update9("fraction", names[n], user_id)
			order = get_order(user_id)
			embedVar = discord.Embed(title=f"Создание заказа №{order['id']}:", description=config.desc_3, color=000000)
			embedVar.add_field(name="Ключ:", value=order['lvl_key'], inline=True)
			embedVar.add_field(name="Цена:", value=str(order['price'])+'₽', inline=True)
			embedVar.add_field(name="Количество людей:", value=order['cnt_executors'], inline=True)
			embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
			message = await member.send(embed=embedVar)
			for emoji in ('➕', '❌'):
				await message.add_reaction(emoji)

		elif emoji in ('➕', '✅') and step == 3:
			order2 = get_order(user_id)
			update9("cnt_roles", order2['cnt_roles']+1, user_id)
			if order2['key_name'] == 'Без ключа':
				update9("step", 2, user_id)
			else:
				update9("step", 5, user_id)
			cnt_executors_fact = order2['cnt_fact_executors']
			update9("cnt_fact_executors", int(cnt_executors_fact)+1, user_id)
			pre_message = await member.fetch_message(payload.message_id)
			await pre_message.delete()
			order = get_order(user_id)
			if order['key_name'] == 'Без ключа':
				embedVar = discord.Embed(title="Создание заказа:", description=config.desc_1, color=000000)
			else:
				embedVar = discord.Embed(title=f"Создание заказа №{order['id']}:", description=config.desc_5, color=000000)
			embedVar.add_field(name="Ключ:", value=order['lvl_key'], inline=True)
			embedVar.add_field(name="Цена:", value=str(order['price'])+'₽', inline=True)
			embedVar.add_field(name="Количество людей:", value=order['cnt_executors'], inline=True)
			embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
			embedVar.add_field(name="Фракция:", value=order['fraction'], inline=True)
			list_roles = system.return_roles(user_id)
			embedVar.add_field(name="Роли:", value=list_roles, inline=True)
			message = await member.send(embed=embedVar)
			if order['key_name'] == 'Без ключа':
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '#️⃣', '*️⃣'):
					await message.add_reaction(emoji)
			else:
				roles = eval(order['roles'])
				values_roles = []
				print(roles)
				for role in roles:
					role1 = roles[role]
					values_roles.append(role1['role'])
				print(values_roles)
				if 'Tank' in values_roles:
					if 'Heal' in values_roles:
						if values_roles.count('Dps') == 1:
							for emoji in ('2️⃣', '❌'):
								await message.add_reaction(emoji)
						else:
							for emoji in ('2️⃣', '❌'):
								await message.add_reaction(emoji)
					elif values_roles.count('Dps') == 1:
						for emoji in ('2️⃣', '3️⃣', '❌'):
							await message.add_reaction(emoji)
					elif values_roles.count('Dps') == 2:
						for emoji in ('3️⃣', '❌'):
							await message.add_reaction(emoji)
					else:
						for emoji in ('2️⃣', '3️⃣', '❌'):
							await message.add_reaction(emoji)
				elif 'Heal' in values_roles:
					if 'Tank' in values_roles:
						for emoji in ('2️⃣', '❌'):
							await message.add_reaction(emoji)
					elif values_roles.count('Dps') == 1:
						for emoji in ('1️⃣', '2️⃣', '❌'):
							await message.add_reaction(emoji)
					elif values_roles.count('Dps') == 2:
						for emoji in ('1️⃣', '❌'):
							await message.add_reaction(emoji)
					else:
						for emoji in ('1️⃣', '2️⃣', '❌'):
							await message.add_reaction(emoji)
				elif values_roles.count('Dps') == 1:
					for emoji in ('1️⃣', '2️⃣', '3️⃣', '❌'):
						await message.add_reaction(emoji)
				elif values_roles.count('Dps') == 2:
					for emoji in ('1️⃣', '3️⃣', '❌'):
						await message.add_reaction(emoji)

		elif emoji in ('1️⃣', '2️⃣', '3️⃣') and step == 5:
			update9("step", 6, user_id)
			names = config.roles
			pre_message = await member.fetch_message(payload.message_id)
			await pre_message.delete()
			order = get_order(user_id)

			if emoji == "1️⃣":
				roles = order['roles']
				for n in names:
					if emoji==n:
						try:
							dict_roles = eval(order['roles'])
							role = dict_roles['0']
							role['role'] = names[n]
							print(dict_roles)
							update9("roles", str(dict_roles), user_id)
						except:
							dict_role = eval(order['roles'])
							role = {}
							role['role'] = names[n]
							dict_role['0'] = role
							print(dict_roles)
							update9("roles", str(dict_role), user_id)

				embedVar = discord.Embed(title=f"Создание заказа №{order['id']}:", description=config.desc_6_tank, color=000000)
				embedVar.add_field(name="Ключ:", value=order['lvl_key'], inline=True)
				embedVar.add_field(name="Цена:", value=str(order['price'])+'₽', inline=True)
				embedVar.add_field(name="Количество людей:", value=order['cnt_executors'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
				embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
				list_roles = system.return_roles(user_id)
				embedVar.add_field(name="Роли:", value=list_roles, inline=True)
				message = await member.send(embed=embedVar)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '❌'):
					await message.add_reaction(emoji)
			else:
				for n in names:
					if emoji==n:
						roles = order['roles']
						for n in names:
							if emoji==n:
								try:
									dict_roles = eval(order['roles'])
									role = dict_roles['0']
									role['role'] = names[n]
									update9("roles", str(dict_roles), user_id)
								except:
									dict_role = eval(order['roles'])
									role = {}
									role['role'] = names[n]
									dict_role['0'] = role
									update9("roles", str(dict_role), user_id)
				
				embedVar = discord.Embed(title=f"Создание заказа №{order['id']}:", description=config.desc_6, color=000000)
				embedVar.add_field(name="Ключ:", value=order['lvl_key'], inline=True)
				embedVar.add_field(name="Цена:", value=str(order['price'])+'₽', inline=True)
				embedVar.add_field(name="Количество людей:", value=order['cnt_executors'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
				embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
				order2 = get_order(user_id)
				list_roles = system.return_roles(user_id)
				embedVar.add_field(name="Роли:", value=list_roles, inline=True)
				message = await member.send(embed=embedVar)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '❌'):
					await message.add_reaction(emoji)
		
		elif emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣') and step == 6:
			update9("step", 3, user_id)
			order = get_order(user_id)
			role = eval(order['roles'])['0']
			if role['role'] == 'Tank':
				names = config.armors_tank
			else:
				names = config.armors_other
			pre_message = await member.fetch_message(payload.message_id)
			await pre_message.delete()

			cnt_role = order['cnt_executors']
			cnt_user = order['cnt_fact_executors']
			for n in names:
				if emoji==n:
					roles = order['roles']
					for n in names:
						if emoji==n:
							dict_roles = eval(order['roles'])
							rol = dict_roles['0']
							rol['armor'] = names[n]
							del dict_roles['0']
							dict_roles[f'{cnt_user}'] = rol
							print(dict_roles)
							update9("roles", str(dict_roles), user_id)
			if cnt_role != cnt_user:
				order2 = get_order(user_id)
				embedVar = discord.Embed(title=f"Создание заказа №{order2['id']}:", description=config.desc_3, color=000000)
				embedVar.add_field(name="Ключ:", value=order2['lvl_key'], inline=True)
				embedVar.add_field(name="Цена:", value=str(order['price'])+'₽', inline=True)
				embedVar.add_field(name="Количество людей:", value=order2['cnt_executors'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order2['key_name'], inline=True)
				embedVar.add_field(name="Фракция", value=order2['fraction'], inline=True)
				list_roles = system.return_roles(user_id)
				embedVar.add_field(name="Роли:", value=list_roles, inline=True)
				message = await member.send(embed=embedVar)
				for emoji in ('➕', '❌'):
					await message.add_reaction(emoji)
			elif cnt_role == cnt_user:
				update9("step", 8, user_id)
				order2 = get_order(user_id)
				list_roles = system.return_roles(user_id)
				embedVar = discord.Embed(title=f"Создание заказа №{order2['id']}:", description='Для завершения заказа оставь комментарий - /comment [текст]', color=000000)
				embedVar.add_field(name="Ключ:", value=order2['lvl_key'], inline=True)
				embedVar.add_field(name="Цена:", value=str(order2['price'])+'₽', inline=True)
				embedVar.add_field(name="Количество людей:", value=order2['cnt_executors'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order2['key_name'], inline=True)
				embedVar.add_field(name="Фракция:", value=order2['fraction'], inline=True)
				embedVar.add_field(name="Роли:", value=list_roles, inline=True)
				embedVar.add_field(name="Комментарий:", value=order2['link'], inline=True)
				embedVar.add_field(name="Цена:", value=order2['price'], inline=True)
				embedVar.add_field(name="Room:", value='#заказы', inline=True)
				message = await member.send(embed=embedVar)

		elif emoji in ('✅', '❌') and step==9:
			if int(payload.channel_id) == 774270476305563679:
				pre_message1 = await channel_orders.fetch_message(payload.message_id)
				order_id = int(pre_message1.content[7:])
				update8('message_order', int(payload.message_id), order_id)
				order = get_order_id(order_id)
				if order['executors_id'] != None:
					list_executors = eval(order['executors_id'])
				else:
					list_executors = []
				
				executor = get_executor(user_id)
				
				if user_id in list_executors:
					message = await member.send(f"Ты уже зарегистрирован в заказе №{order_id}")

				elif executor == {}:
					message = await member.send(f"Тебя еще нет в базе.\nДля регистрации отправь /cab")
				else:
					if len(list_executors) != order['cnt_executors']:
						embedVar = discord.Embed(title="Подтверждение заказа:", description='Данные заказа', color=000000)
						embedVar.add_field(name="Ключ:", value=order['lvl_key'], inline=True)
						embedVar.add_field(name="Количество людей:", value=order['cnt_executors'], inline=True)
						embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
						embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
						list_roles = system.return_roles(user_id)
						embedVar.add_field(name="Роли:", value=list_roles, inline=True)
						embedVar.add_field(name="Room:", value='Заказы', inline=True)
						embedVar.add_field(name="Ссылка:", value=order['link'], inline=True)
						embedVar.add_field(name="Цена:", value=str(int(order['price'])/int(order['cnt_executors']))+'₽', inline=True)
						embedVar.add_field(name="Подвердить заказ:", value=config.desc_9, inline=True)
						message = await member.send(f"Заказ №{order_id}", embed=embedVar)
						if len(eval(order['roles'])) == 1:
							for emoji in ('1️⃣'):
								await message.add_reaction(emoji)
						elif len(eval(order['roles'])) == 2:
							for emoji in ('1️⃣', '2️⃣'):
								await message.add_reaction(emoji)
						elif len(eval(order['roles'])) == 3:
							for emoji in ('1️⃣', '2️⃣', '3️⃣'):
								await message.add_reaction(emoji)
						elif len(eval(order['roles'])) == 4:
							for emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣'):
								await message.add_reaction(emoji)
					else:
						pre_message = await channel_orders.fetch_message(payload.message_id)
						await pre_message.delete()
						order_id = int(pre_message.content[7:])
						await channel_orders.send(f"В заказ №{order_id} набрано максимальное количество участников.")
			else:
				pre_message1 = await member.fetch_message(payload.message_id)
				integ = system.return_digits(pre_message1.content)
				order_id = integ[1]
				order = get_order_id(order_id)
				customer = bot.get_user(order['customer_id'])
				if order['executors_id'] != None:
					list_executors = eval(order['executors_id'])
					list_executors.append(user_id)
				else:
					list_executors = []
					list_executors.append(user_id)
				update8('executors_id', str(list_executors), order_id)
				roles = eval(order['roles'])
				del roles[str(integ[0])]
				update8('roles', str(roles), order_id)
				embedVar = discord.Embed(title=f"Ты зарегистрирован в заказ №{order_id}", description='Ссылка-приглашение: тут ссылка', color=000000)
				await customer.send(f"В заказ №{order_id} зарегистрировался {user_name}")
				await member.send(embed=embedVar)
				order2 = get_order_id(order_id)
				update("executors", "balance", int(order2['price'])/int(order2['cnt_executors']), user_id)
				try:
					pre_message = await channel_orders.fetch_message(str(order['message_order']))
					list_roles = system.return_roles(user_id)
					embedVar_order = discord.Embed(title="Новый заказ:", description=f"№{order2['id']} - {order2['key_name']}", color=000000)
					embedVar_order.add_field(name="Количество людей:", value=order2['cnt_executors'], inline=True)
					embedVar_order.add_field(name="Фракция:", value=order2['fraction'], inline=True)
					embedVar_order.add_field(name="Роли:", value=list_roles, inline=True)
					embedVar_order.add_field(name="Cсылка:", value=order2['link'], inline=True)
					embedVar_order.add_field(name="Цена:", value=str(order['price'])+'₽', inline=True)
					await pre_message.edit(embed=embedVar_order)
				except:
					# names_executors = eval(order2[])
					pre_message = await channel_orders.fetch_message(str(order['message_order']))
					await pre_message.delete()
					await channel_orders.send(f"В заказ №{order_id} набрано максимальное количество участников.")
					await customer.send(f"Заказ №{order_id} собран и начат.")

		elif emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣') and step==9:
			print(user_id, payload.message_id)
			pre_message = await member.fetch_message(payload.message_id)
			await pre_message.delete()
			order_id = int(pre_message.content[7:])
			order = get_order_id(order_id)
			roles = eval(order['roles'])
			if emoji == '1️⃣':
				role = roles['1']
				item_str = f"{role['role']}-{role['armor']}-{role['key']}"
			elif emoji == '2️⃣':
				role = roles['2']
				item_str = f"{role['role']}-{role['armor']}-{role['key']}"
			elif emoji == '3️⃣':
				role = roles['3']
				item_str = f"{role['role']}-{role['armor']}-{role['key']}"
			elif emoji == '4️⃣':
				role = roles['4']
				item_str = f"{role['role']}-{role['armor']}-{role['key']}"
			
			embedVar = discord.Embed(title="Действия:", description=config.desc_8, color=000000)
			embedVar.add_field(name="Роль:", value=item_str, inline=True)

			if emoji == '1️⃣':
				message = await member.send(f"Подтверждение на регистрацию роли №1 в заказе №{order_id}", embed=embedVar)
			elif emoji == '2️⃣':
				message = await member.send(f"Подтверждение на регистрацию роли №2 в заказе №{order_id}", embed=embedVar)
			elif emoji == '3️⃣':
				message = await member.send(f"Подтверждение на регистрацию роли №3 в заказе №{order_id}", embed=embedVar)
			elif emoji == '4️⃣':
				message = await member.send(f"Подтверждение на регистрацию роли №4 в заказе №{order_id}", embed=embedVar)
			await message.add_reaction('✅')
			await message.add_reaction('❌')

		elif emoji == '❌' and step in (1, 2, 3, 5, 6, 7, 8):
			update9("step", 11, user_id)
			embedVar = discord.Embed(title="Заказ отменен", description=config.desc_7, color=000000)
			message = await member.send(embed=embedVar)
		else:
			pass


if __name__ == '__main__':
    bot.run(config.TOKEN)

