from db import get_order_id, get_order


def return_roles(order_id: int):
	try:
		order = get_order_id(order_id)
		print(order)
		list_roles = []
		raw_roles = eval(order['roles'])
		print(raw_roles)
		emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
		for r, e in zip(raw_roles, emoji):
			item = raw_roles[r]
			try:
				item_str = f"{e} {item['role']}-{item['armor']}-{item['key']}"
			except:
				try:
					item_str = f"{e} {item['role']}-{item['armor']}"
				except:
					item_str = f"{e} {item['role']}"
			list_roles.append(item_str)
		roles = '\n'.join(list_roles)
	except:
		roles = 'Не указано'
	return roles


def return_digits(content):
	s = content
	l = len(s)
	integ = []
	i = 0
	while i < l:
		s_int = ''
		a = s[i]
		while '0' <= a <= '9':
			s_int += a
			i += 1
			if i < l:
				a = s[i]
			else:
				break
		i += 1
		if s_int != '':
			integ.append(int(s_int))
	return integ

